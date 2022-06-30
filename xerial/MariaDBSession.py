from xerial.DBSessionBase import DBSessionBase, PrimaryDataError
from xerial.IntegerColumn import IntegerColumn

import logging

try :
	import mariadb
except :
	logging.warning("Module mariadb cannot be imported.")

class MariaDBSession (DBSessionBase) :
	def createConnection(self):
		self.connection = mariadb.connect(
			user=self.config["user"],
			password=self.config["password"],
			host=self.config["host"],
			port=self.config["port"],
			database=self.config["database"]
		)
		self.cursor = self.connection.cursor()
	
	def closeConnection(self) :
		self.connection.close()
	
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
		modelClass.__select_column__ = ", ".join([i[0] for i in modelClass.meta])
		modelClass.__insert_column__ = ", ".join([i[0] for i in meta ])
		modelClass.__insert_parameter__ = ", ".join(["?"]*len(meta))
		modelClass.__all_column__ = ", ".join([i[0] for i in modelClass.meta])
		modelClass.__all_parameter__ = ", ".join(["?"]*len(modelClass.meta))
		modelClass.__update_set_parameter__  = ", ".join(["%s=?"%(m[0]) for m in meta])
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
			logging.error(query)
			logging.error(parameter)
			self.closeConnection()
			self.connect()
			raise error
	
	def executeRegularWrite(self, query, parameter=None):
		return self.executeRead(query, parameter)

	def generateCountQuery(self, modelClass, clause) :
		if isinstance(modelClass.primary, list):
			return "SELECT COUNT(%s) AS COUNTED FROM %s %s"%(', '.join(modelClass.primary), modelClass.__fulltablename__, clause)
		else:
			return "SELECT COUNT(%s) AS COUNTED FROM %s %s"%(modelClass.primary, modelClass.__fulltablename__, clause)
		
	def generateSelectQuery(self, modelClass, clause, limit=None, offset=None) :
		limitClause = "" if limit is None else "LIMIT %d"%(limit)
		offsetClause = "" if offset is None else "OFFSET %d"%(offset)
		return "SELECT %s FROM %s %s %s %s"%(
			modelClass.__select_column__,
			modelClass.__fulltablename__,
			clause, limitClause, offsetClause
		)
	
	def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		value = self.getRawValue(record, isAutoID)
		query = self.generateInsert(modelClass)
		cursor = self.executeWrite(query, value)
		if modelClass.__is_increment__ :
			setattr(record, modelClass.primary, self.cursor.lastrowid)
			return cursor.lastrowid
	
	def generateInsert(self, modelClass, isAutoID=True) :
		if isAutoID :
			return "INSERT INTO %s(%s) VALUES(%s)"%(
				modelClass.__fulltablename__,
				modelClass.__insert_column__,
				modelClass.__insert_parameter__
			)
		else :
			return "INSERT INTO %s(%s) VALUES(%s)"%(
				modelClass.__fulltablename__,
				modelClass.__all_column__,
				modelClass.__all_parameter__
			)
	
	def insertMultiple(self, recordList, isAutoID=True) :
		if len(recordList) == 0 : return
		valueList = []
		modelClass = None
		for record in recordList :
			valueList.append(tuple(self.getRawValue(record, isAutoID)))
			modelClass = record.__class__
		
		query = self.generateInsert(modelClass, isAutoID)
		try :
			cursor = self.connection.writeCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
		except Exception as error :
			logging.debug(query)
			logging.debug(valueList)
			self.closeConnection()
			self.connect()
			raise error

	def update(self, record) :
		value = self.getRawValue(record)
		modelClass = record.__class__
		query = self.generateUpdate(modelClass)
		self.executeWrite(query, value)

	def generateUpdate(self, modelClass) :
		return "UPDATE %s SET %s WHERE %s"%(
			modelClass.__fulltablename__,
			modelClass.__update_set_parameter__,
			self.getPrimaryClause(record)
		)
	
	def drop(self, record) :
		table = record.__fulltablename__
		query = "DELETE FROM %s WHERE %s"%(table, self.getPrimaryClause(record))
		self.executeWrite(query)
	
	def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be dropped by ID.")
			return
		table = modelClass.__fulltablename__
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s WHERE %s=%s"%(table, modelClass.primary, ID)
		self.executeWrite(query)
	
	def dropByCondition(self, modelClass, clause) :
		table = modelClass.__fulltablename__
		query = "DELETE FROM %s WHERE %s"%(table, clause)
		self.executeWrite(query)
	
	def createTable(self) :
		self.getExistingTable()
		for model in self.model.values() :
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__fulltablename__ in self.existingTable :
				self.createIndex(model)
				continue
			query = self.generateCreateTable(model)
			self.executeWrite(query)
			self.createIndex(model)
	
	def generateCreateTable(self, model) :
		columnList = []
		isIncremental = model.__is_increment__
		isPrimaryList = hasattr(model, 'primaryMeta') and isinstance(model.primaryMeta, list)
		primaryList = []
		for name, column in model.meta :
			if not (isIncremental and column.isPrimary) :
				primary = ""
				if column.isPrimary :
					if isPrimaryList : primaryList.append(name)
					else : primary = "PRIMARY KEY"
				notNull = "NOT NULL" if column.isNotNull else ""
				isDefault = hasattr(column, 'default') and column.default is not None
				default = "DEFAULT %s"%(column.setValueToDB(column.default)) if isDefault else ""
				columnList.append(f"{name} {column.getDBDataType()} {primary} {default} {notNull}")
		query = [f"CREATE TABLE {model.__fulltablename__} (\n\t"]
		if len(primaryList) :
			columnList.append("PRIMARY KEY(%s)"%(",".join(primaryList)))
		if isIncremental :
			columnList.insert(0, "%s INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT"%(model.primary))
		
		query.append(",\n\t".join(columnList))
		query.append(") ENGINE=MyISAM;")
		return " ".join(query)

	def createIndex(self, model) :
		result = self.executeRead("SHOW INDEX FROM %s"%(model.__fulltablename__))
		exisitingIndex = {i[4] for i in result}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				self.executeWrite("CREATE INDEX %s_%s ON %s(%s)"%(model.__fulltablename__, name, model.__fulltablename__, name))
	
	def getExistingTable(self) :
		result = self.executeRead("SHOW TABLES")
		self.existingTable = {row[0] for row in result}
		return self.existingTable
			