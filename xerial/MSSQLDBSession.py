from xerial.DBSessionBase import DBSessionBase, PrimaryDataError
from xerial.IntegerColumn import IntegerColumn

import logging, time

try :
	import pyodbc
except :
	logging.warning("Module pyodbc cannot be imported.")

"""
Install MS SQL Docker

sudo docker pull mcr.microsoft.com/mssql/server:2019-latest
sudo docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=SECRET_PASSWORD" \
   -p 1433:1433 --name mssqlserver --hostname mssqlserver \
   -d mcr.microsoft.com/mssql/server:2019-latest

Default User : SA

Full documentation

https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash

Installation of MS SQL Server Driver for ODBC

https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15

"""

class MSSQLDBSession (DBSessionBase) :
	def createConnection(self):
		self.connection = pyodbc.connect(f"""
			DRIVER={{{self.config['driver']}}};
			SERVER={self.config['host']};
			DATABASE={self.config['database']};
			UID={self.config['user']};
			PWD={self.config['password']};
			TrustServerCertificate=yes;
		""", autocommit=True)
		self.cursor = self.connection.cursor()
		self.isOpened = True
	
	def closeConnection(self) :
		self.connection.close()
		self.cursor.close()
		self.isOpened = False
	
	def generateSelectQuery(self, modelClass, clause, limit=None, offset=None) :
		if 'order by' not in clause.lower() :
			clause += f' ORDER BY {modelClass.primary}'
		if limit is not None and offset is None :
			limitClause = "FETCH FIRST %d ROWS ONLY"%(limit)
			offsetClause = "OFFSET 0 ROWS"
		else :
			limitClause = "" if limit is None else "FETCH NEXT %d ROWS ONLY"%(limit)
			offsetClause = "" if offset is None else "OFFSET %d ROWS"%(offset)

		return "SELECT %s FROM %s %s %s %s"%(
			modelClass.__select_column__,
			modelClass.__full_table_name__,
			clause, offsetClause, limitClause
		)

	def generateRawSelectQuery(self, tableName, clause, limit=None, offset=None) :
		if 'order by' not in clause.lower() :
			clause += f' ORDER BY id'
		if limit is not None and offset is None :
			limitClause = "FETCH FIRST %d ROWS ONLY"%(limit)
			offsetClause = "OFFSET 0 ROWS"
		else :
			limitClause = "" if limit is None else "FETCH NEXT %d ROWS ONLY"%(limit)
			offsetClause = "" if offset is None else "OFFSET %d ROWS"%(offset)

		return "SELECT * FROM %s %s %s %s"%(
			tableName,
			clause, offsetClause, limitClause
		)

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
			logging.debug(query)
			logging.debug(parameter)
			self.closeConnection()
			self.connect()
			raise error
	
	def executeRegularWrite(self, query, parameter=None):
		return self.executeRead(query, parameter)

	def generateCountQuery(self, modelClass, clause) :
		if isinstance(modelClass.primary, list):
			return "SELECT COUNT(%s) AS COUNTED FROM %s %s"%(
				', '.join(modelClass.primary),
				modelClass.__full_table_name__,
				clause
			)
		else:
			return "SELECT COUNT(%s) AS COUNTED FROM %s %s"%(
				modelClass.primary,
				modelClass.__full_table_name__,
				clause
			)
			
	def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = -1.0
		value = self.getRawValue(record, isAutoID)
		query = self.generateInsert(modelClass)
		if not isAutoID and modelClass.__is_increment__:
			self.executeWrite(f"SET IDENTITY_INSERT {modelClass.__full_table_name__} ON;")
		cursor = self.executeWrite(query, value)	
		if not isAutoID and modelClass.__is_increment__ :
			self.executeWrite(f"SET IDENTITY_INSERT {modelClass.__full_table_name__} OFF;")
		elif not isAutoID :
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			insertedID = cursor.fetchone()[0]
			setattr(record, modelClass.primary, insertedID)
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
			return insertedID
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
		
		query = self.generateInsert(modelClass, isAutoID)
		try :
			if not isAutoID and modelClass.__is_increment__ :
				self.executeWrite(f"SET IDENTITY_INSERT {modelClass.__full_table_name__} ON;")
			cursor = self.connection.writeCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
			if not isAutoID and modelClass.__is_increment__ :
				self.executeWrite(f"SET IDENTITY_INSERT {modelClass.__full_table_name__} OFF;")
		except Exception as error :
			logging.debug(query)
			logging.debug(valueList)
			self.closeConnection()
			self.connect()
			raise error
	
	def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		query = self.generateInsert(modelClass, isAutoID=False)
		try :
			if modelClass.__is_increment__ :
				self.executeWrite(f"SET IDENTITY_INSERT {modelClass.__full_table_name__} ON;")
			cursor = self.connection.writeCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
			if modelClass.__is_increment__ :
				self.executeWrite(f"SET IDENTITY_INSERT {modelClass.__full_table_name__} OFF;")
		except Exception as error :
			logging.debug(query)
			logging.debug(valueList)
			self.closeConnection()
			self.connect()
			raise error


	def generateInsert(self, modelClass, isAutoID=True) :
		if isAutoID :
			if  modelClass.__is_increment__ :
				return "SET NOCOUNT ON; DECLARE @NEWID TABLE(ID INT); INSERT INTO %s(%s) OUTPUT inserted.id INTO @NEWID(ID) VALUES(%s); SELECT ID FROM @NEWID;"%(
					modelClass.__full_table_name__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__
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
		query = self.generateUpdateQuery(record)
		self.executeWrite(query, value)
		if len(modelClass.children) :
			self.updateChildren(record, modelClass)
	
	def updateDirect(self, modelClass, raw) :
		value = self.toTuple(modelClass, raw)
		query = self.generateRawUpdateQuery(modelClass, raw)
		self.executeWrite(query, value)
	
	def generateUpdateQuery(self, record) :
		modelClass = record.__class__
		return "UPDATE %s SET %s WHERE %s"%(
			modelClass.__full_table_name__,
			modelClass.__update_set_parameter__,
			self.getPrimaryClause(record)
		)
	
	def generateRawUpdateQuery(self, modelClass, raw) :
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
			if model.__full_table_name__ in self.existingTable :
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
		query = [f"CREATE TABLE {model.__full_table_name__} (\n\t"]
		if isIncremental :
			columnList.insert(0, "%s INTEGER IDENTITY(1,1) PRIMARY KEY"%(model.primary))
		
		query.append(",\n\t".join(columnList))
		query.append(")")
		return " ".join(query)

	def createIndex(self, model) :
		result = self.executeRead(self.generateIndexQuery(model))
		exisitingIndex = {i[0] for i in result}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				self.executeWrite("CREATE INDEX %s_%s ON %s(%s)"%(model.__full_table_name__, name, model.__full_table_name__, name))
	
	def generateIndexQuery(self, model) :
		return f"""
		SELECT
			COL_NAME(b.object_id, b.column_id) AS Column_Name
		FROM
			sys.indexes AS a
		INNER JOIN
			sys.index_columns AS b
			ON a.object_id = b.object_id AND a.index_id = b.index_id
		WHERE
			a.is_hypothetical = 0 AND
			a.is_primary_key != 1 AND
			a.object_id = OBJECT_ID('{model.__full_table_name__}');
		"""
	
	def getExistingTable(self) :
		result = self.executeRead("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
		self.existingTable = {row[0] for row in result}
		return self.existingTable
	
	def generateResetID(self, modelClass:type) -> str :
		return f"DBCC CHECKIDENT ('{modelClass.__full_table_name__}', RESEED, ?);"