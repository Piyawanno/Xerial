from xerial.DBSessionBase import DBSessionBase, PrimaryDataError
from xerial.IntegerColumn import IntegerColumn
from typing import Dict, Any, List

import logging, sqlite3, traceback, time

class SQLiteDBSession (DBSessionBase) :
	def createConnection(self):
		self.connection = sqlite3.connect(self.config["database"], isolation_level=None, check_same_thread=False)
		self.cursor = self.connection.cursor()
		self.isOpened = True
	
	def closeConnection(self) :
		self.connection.close()
		self.isOpened = False
	
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
		modelClass.__select_column__ = ", ".join([f'{table}.{i[0]}' for i in modelClass.meta])
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
			print(query)
			print(parameter)
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
		
	def generateSelectQuery(self, modelClass, clause, limit=None, offset=None) :
		limitClause = "" if limit is None else "LIMIT %d"%(limit)
		offsetClause = "" if offset is None else "OFFSET %d"%(offset)
		return "SELECT %s FROM %s %s %s %s"%(
			modelClass.__select_column__,
			modelClass.__full_table_name__,
			clause, limitClause, offsetClause
		)
	
	def generateRawSelectQuery(self, tableName, clause, limit=None, offset=None) :
		limitClause = "" if limit is None else "LIMIT %d"%(limit)
		offsetClause = "" if offset is None else "OFFSET %d"%(offset)
		return "SELECT * FROM %s %s %s %s"%(
			tableName,
			clause, limitClause, offsetClause
		)

	def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		query = self.generateInsertQuery(modelClass, isAutoID)
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = -1.0
		value = self.getRawValue(record, isAutoID)
		cursor = self.executeWrite(query, value)
		if not isAutoID :
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			setattr(record, modelClass.primary, self.cursor.lastrowid)
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
			return cursor.lastrowid
		elif len(modelClass) > 0 :
			logging.warning(f"Primary key of {modelClass.__table_name__} is not auto generated. Children cannot be inserted.")

	def generateInsertQuery(self, modelClass, isAutoID=True) :
		if isAutoID :
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
		query = self.generateInsertQuery(modelClass, isAutoID)
		try :
			cursor = self.connection.writerCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
		except Exception as error :
			print(query)
			print(valueList)
			logging.error(query)
			logging.error(valueList)
			self.closeConnection()
			self.connect()
			raise error
	
	def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		query = self.generateInsertQuery(modelClass, isAutoID=False)
		try :
			cursor = self.connection.writerCursor if self.isRoundRobin else self.cursor
			cursor.executemany(query, valueList)
		except Exception as error :
			print(query)
			print(valueList)
			logging.error(query)
			logging.error(valueList)
			self.closeConnection()
			self.connect()
			raise error
	
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
		query = [f"CREATE TABLE IF NOT EXISTS {model.__full_table_name__} (\n\t"]
		if isIncremental :
			columnList.insert(0, "%s INTEGER PRIMARY KEY AUTOINCREMENT"%(model.primary))
		
		query.append(",\n\t".join(columnList))
		query.append(")")
		return " ".join(query)

	def createIndex(self, model) :
		query = self.generateIndexCheckQuery(model)
		cursor = self.executeWrite(query)
		exisitingIndex = {i[0] for i in cursor}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				self.executeWrite(self.generateIndexQuery(model, name))
	
	def generateIndexQuery(self, model, columnName) :
		return "CREATE INDEX IF NOT EXISTS %s_%s ON %s(%s)"%(
			model.__full_table_name__, columnName,
			model.__full_table_name__, columnName
		)

	def getExistingTable(self) :
		result = self.executeRead(self.generateTableQuery())
		self.existingTable = {row[0] for row in result}
		return self.existingTable

	def generateTableQuery(self) :
		return 'SELECT name FROM sqlite_master WHERE type = "table"'

	def generateIndexCheckQuery(self, model) :
		return f'SELECT name FROM sqlite_master WHERE type = "index" AND tbl_name="{model.__full_table_name__}"'
	
	def generateResetID(self, modelClass:type) -> str :
		return f"UPDATE SQLITE_SEQUENCE SET SEQ=? WHERE NAME='{modelClass.__full_table_name__}';"
		