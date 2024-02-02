from xerial.DBSessionBase import DBSessionBase
from xerial.IntegerColumn import IntegerColumn

import logging, time

try :
	import cx_Oracle
except :
	logging.warning("Module cx_Oracle cannot be imported.")

"""
Client Installation

https://gist.github.com/bmaupin/1d376476a2b6548889b4dd95663ede58

Docker Test Environment

$ sudo docker pull gvenzl/oracle-xe
$ sudo docker run -e ORACLE_PASSWORD='SECRET_PASSWORD' \
	-e ORACLE_DATABASE='DB_NAME' \
	-e APP_USER='APP_USER' \
	-e APP_USER_PASSWORD='SECRET_PASSWORD' \
	-p 1521:1521 \
	--name oracledb -d gvenzl/oracle-xe

domain : XEPDB1

Docker Full Document

https://hub.docker.com/r/gvenzl/oracle-xe

"""

class OracleDBSession (DBSessionBase) :
	def createConnection(self):
		self.connection = cx_Oracle.connect('%s/%s@%s:%d/%s'%(
			self.config['user'],
			self.config["password"],
			self.config["host"],
			self.config["port"],
			self.config["domain"],
		))
		self.connection.autocommit = True
		self.cursor = self.connection.cursor()
		self.isOpened = True

	def closeConnection(self) :
		self.connection.close()
		self.isOpened = False
	
	def processClause(self, clause: str, parameter:list) -> str:
		n = 1
		p = 0
		processed = []
		while True :
			i = clause.find("?", p)
			if i < 0 :
				if p == 0 : return clause
				else : break
			processed.append(clause[p:i])
			processed.append(f":{n}")
			p = i+1
			n = n+1
		return "".join(processed)
	
	def prepareStatement(self, modelClass) :
		if hasattr(modelClass, 'primaryMeta') :
			primary = modelClass.primaryMeta
			if not hasattr(modelClass, '__is_increment__') :
				modelClass.__is_increment__ = isinstance(primary, IntegerColumn)
		else :
			modelClass.__is_increment__ = False
		if modelClass.__is_increment__ :
			meta = [i for i in modelClass.meta if i[1] != primary]
		else :
			meta = modelClass.meta
		table = modelClass.__full_table_name__.lower()
		modelClass.__select_column__ = ", ".join([f'{table}{i[0]}' for i in modelClass.meta])
		modelClass.__insert_column__ = ", ".join([i[0] for i in meta ])
		modelClass.__insert_parameter__ = ", ".join([":%d"%(i+1) for i, m in enumerate(meta)])
		modelClass.__all_column__ = ", ".join([i[0] for i in modelClass.meta])
		modelClass.__all_parameter__ = ", ".join([":%d"%(i+1) for i, m in enumerate(modelClass.meta)])
		modelClass.__update_set_parameter__  = ", ".join(["%s=:%d"%(m[0], i) for i, m in enumerate(meta) ])
		if modelClass.__is_increment__ :
			modelClass.insertMeta = [i for i in modelClass.meta if i[1] != primary]
		else :
			modelClass.insertMeta = modelClass.meta

	def executeRoundRobinRead(self, query, parameter=None) :
		self.queryCount += 1
		cursor = self.connection.getNextReadCursor()
		try :
			if parameter is None :
				cursor.execute(query)
			else :
				cursor.execute(query, parameter)
			return cursor
		except Exception as error :
			logging.debug(query)
			logging.debug(parameter)
			self.closeConnection()
			self.connect()
			raise error
	
	def executeRoundRobinWrite(self, query, parameter=None) :
		self.queryCount += 1
		cursor = self.connection.writerCursor
		try :
			if parameter is None :
				cursor.execute(query)
			else :
				cursor.execute(query, parameter)
			return cursor
		except Exception as error :
			logging.debug(query)
			logging.debug(parameter)
			self.closeConnection()
			self.connect()
			raise error

	def executeRegularRead(self, query, parameter=None) :
		self.queryCount += 1
		try :
			if parameter is None :
				self.cursor.execute(query)
			else :
				self.cursor.execute(query, parameter)
			return self.cursor
		except Exception as error :
			logging.debug(query)
			self.closeConnection()
			self.connect()
			raise error
	
	def executeRegularWrite(self, query, parameter=None):
		return self.executeRead(query, parameter)

	def generateCountQuery(self, modelClass, clause) :
		return 'SELECT COUNT(%s) "COUNTED" FROM %s %s'%(modelClass.primary, modelClass.__full_table_name__, clause)
		
	def generateSelectQuery(self, modelClass, clause, limit=None, offset=None) :
		if limit is not None :
			if offset is None : offset = 0
			limitClause = "OFFSET %d ROWS FETCH NEXT %d ROWS ONLY"%(offset, limit)
		else :
			limitClause = ""
		return "SELECT %s FROM %s %s %s"%(
			modelClass.__select_column__,
			modelClass.__full_table_name__,
			clause, limitClause
		)
	
	def generateRawSelectQuery(self, tableName, clause, limit=None, offset=None) :
		if limit is not None :
			if offset is None : offset = 0
			limitClause = "OFFSET %d ROWS FETCH NEXT %d ROWS ONLY"%(offset, limit)
		else :
			limitClause = ""
		return "SELECT * FROM %s %s %s"%(
			tableName,
			clause, limitClause
		)
	
	def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		query = self.generateInsert(modelClass, isAutoID)
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = -1.0
		parameter = self.getRawValue(record, isAutoID)
		if modelClass.__insert_parameter__ :
			insertedID = self.cursor.var(cx_Oracle.NUMBER)
			parameter.append(insertedID)
		self.executeWrite(query, parameter)
		if not isAutoID :
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			lastRow = insertedID.values[0][0]
			setattr(record, modelClass.primary, lastRow)
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
			return lastRow
		elif len(modelClass) > 0 :
			logging.warning(f"Primary key of {modelClass.__table_name__} is not auto generated. Children cannot be inserted.")
		
	def insertMultiple(self, recordList, isAutoID=True, isReturningID=False) :
		if len(recordList) == 0 : return
		if isAutoID and isReturningID :
			return [self.insert(record) for record in recordList]
		valueList = []
		modelClass = None
		hasChildren = False
		for record in recordList :
			if modelClass is None :
				modelClass = record.__class__
				isBackup = modelClass.__backup__
				now = time.time()
				query = self.generateInsert(modelClass, isAutoID, isMultiple=True)
				if len(modelClass.children) :
					hasChildren = True
					break
			if isBackup :
				record.__insert_time__ = now
				record.__update_time__ = -1.0
			valueList.append(self.getRawValue(record, isAutoID))

		if hasChildren :
			for record in recordList :
				self.insert(record)
			return
		try :
			cursor = self.connection.writerCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
		except Exception as error :
			logging.debug(query)
			self.closeConnection()
			self.connect()
			raise error
	
	def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		query = self.generateInsert(modelClass, isAutoID=False, isMultiple=True)
		try :
			cursor = self.connection.writerCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
		except Exception as error :
			logging.debug(query)
			self.closeConnection()
			self.connect()
			raise error
	
	def generateInsert(self, modelClass, isAutoID=True, isMultiple=False) :
		if isAutoID :
			if modelClass.__is_increment__ and not isMultiple:
				return "INSERT INTO %s(%s) VALUES(%s) RETURNING %s INTO :%d"%(
					modelClass.__full_table_name__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__,
					modelClass.primaryMeta.name,
					len(modelClass.meta)
				)
			else :
				return "INSERT INTO %s(%s) VALUES(%s)"%(
					modelClass.__full_table_name__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__
				)
		else :
			return "INSERT INTO %s(%s) VALUES(%s)"%(
				modelClass.__full_table_name__,
				modelClass.__all_column__,
				modelClass.__all_parameter__
			)

	def update(self, record) :
		modelClass = record.__class__
		if modelClass.__backup__ :
			record.__update_time__ = time.time()
		value = self.getRawValue(record)
		self.executeWrite(self.generateUpdate(record), value)
		if len(modelClass.children) :
			self.updateChildren(record, modelClass)
	
	def updateDirect(self, modelClass, raw) :
		value = self.toTuple(modelClass, raw)
		query = self.generateRawUpdate(modelClass, raw)
		self.executeWrite(query, value)
	
	def generateUpdate(self, record) :
		modelClass = record.__class__
		return "UPDATE %s SET %s WHERE %s"%(
			modelClass.__full_table_name__,
			modelClass.__update_set_parameter__,
			self.getPrimaryClause(record)
		)

	def generateRawUpdate(self, modelClass, raw) :
		return "UPDATE %s SET %s WHERE %s"%(
			modelClass.__full_table_name__,
			modelClass.__update_set_parameter__,
			self.getRawPrimaryClause(modelClass, raw)
		)
	
	def drop(self, record) :
		self.dropChildren(record, record.__class__)
		table = record.__full_table_name__
		query = "DELETE FROM %s WHERE %s"%(table, self.getPrimaryClause(record))
		self.executeWrite(query)
	
	def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__full_table_name__} has not primary key and cannot be dropped by ID.")
			return
		self.dropChildrenByID(ID, modelClass)
		table = modelClass.__full_table_name__
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s WHERE %s=%s"%(table, modelClass.primary, ID)
		self.executeWrite(query)
	
	def dropByCondition(self, modelClass, clause) :
		table = modelClass.__full_table_name__
		parentQuery = f"SELECT {modelClass.primary} FROM {table} {clause}"
		for child in modelClass.children :
			childTable = child.model.__full_table_name__
			query = f"DELETE FROM {childTable} WHERE {child.column} IN ({parentQuery})"
			self.executeWrite(query)
		query = "DELETE FROM %s WHERE %s"%(table, clause)
		self.executeWrite(query)
	
	def createTable(self) :
		self.getExistingTable()
		for model in self.model.values() :
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__table_name__.upper() in self.existingTable : continue
			query = self.generateCreatTable(model)
			logging.info(f"Creating Table {model.__table_name__}")
			self.executeWrite(query)
		self.getExistingTable()

		for model in self.model.values() :
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__table_name__.upper() in self.existingTable :
				self.createIndex(model)
	
	def generateCreatTable(self, model) :
		columnList = []
		primaryList = []
		isIncremental = model.__is_increment__
		for name, column in model.meta :
			if not (isIncremental and column.isPrimary) :
				notNull = "NOT NULL" if column.isNotNull else ""
				isDefault = hasattr(column, 'default') and column.default is not None
				default = "DEFAULT %s"%(column.setValueToDB(column.default)) if isDefault else ""
				columnList.append(f"{name} {column.getDBDataType()} {default} {notNull}")
			if column.isPrimary :
				primaryList.append(name)
		if len(primaryList) :
			joined = ",".join(primaryList)
			columnList.append(f"CONSTRAINT {model.__table_name__}_PK PRIMARY KEY ({joined})")
		query = [f"CREATE TABLE {model.__table_name__} ( "]
		if isIncremental :
			columnList.insert(0, "%s INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 1 INCREMENT BY 1)"%(model.primary))
		query.append(",\n".join(columnList))
		query.append(")")
		return "".join(query)
	
	def createIndex(self, model) :
		self.executeRead(self.generateIndexQuery(model))
		existingIndex =  {i[0].upper() for i in self.cursor}
		for name, column in model.meta :
			name = name.upper()
			if column.isIndex and name not in existingIndex:
				self.executeWrite(self.generateCreateIndex(model, name))
	
	def generateIndexQuery(self, model) :
		return """SELECT ind_col.column_name, ind.table_name
		FROM sys.all_indexes ind
		INNER JOIN 
			sys.all_ind_columns ind_col ON ind.owner = ind_col.index_owner 
			AND ind.index_name = ind_col.index_name
		WHERE ind.owner in ('%s') AND ind.table_name='%s'
		"""%("', '".join(self.config['owner']), model.__table_name__.upper())
	
	def generateCreateIndex(self, model, columnName) :
		tableName = model.__table_name__.upper()
		return "CREATE INDEX %s_%s ON %s(%s)"%(tableName, columnName, tableName, columnName)

	def getExistingTable(self) :
		self.executeRead(self.generateCheckTable())
		self.owner = {row[0]:row[1] for row in self.cursor}
		self.existingTable = list(self.owner.keys())
		for model in self.model.values() :
			tableName = model.__table_name__.upper()
			owner = self.owner.get(tableName)
			if owner is not None :
				model.__full_table_name__ = f"{owner}.{tableName}"
			else :
				model.__full_table_name__ = tableName
		return self.existingTable
	
	def generateCheckTable(self) :
		joined = "', '".join(self.config['owner'])
		return f"SELECT table_name, owner  from all_tables WHERE owner IN ('{joined}')"

	def generateResetID(self, modelClass:type) -> str :
		return f"ALTER TABLE {modelClass.__full_table_name__} MODIFY(ID GENERATED AS IDENTITY (START WITH ?));"