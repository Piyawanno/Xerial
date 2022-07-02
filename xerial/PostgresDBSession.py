from xerial.DBSessionBase import DBSessionBase, PrimaryDataError
from xerial.IntegerColumn import IntegerColumn

import logging

try :
	import psycopg2
	import psycopg2.extras
except :
	logging.warning("Module psycopg2 cannot be imported.")

class PostgresDBSession (DBSessionBase) :
	def __init__(self, config) :
		DBSessionBase.__init__(self, config)
		self.schema = ""
	
	def setSchema(self, schema) :
		self.schema = f"{schema.lower()}."
	
	def createSchema(self, schema) :
		query = self.generateCreateSchema(schema)
		self.executeWrite(query)
	
	def generateCreateSchema(self, schema) :
		return f"CREATE SCHEMA IF NOT EXISTS {schema.lower()}"
	
	def checkTableName(self, modelClass) :
		prefix = self.prefix
		if not hasattr(modelClass, '__tablename__') :
			modelClass.__tablename__ = f"{prefix}{modelClass.__name__}"
		tableName = modelClass.__tablename__
		if prefix is not None and len(prefix) :
			if tableName[:len(prefix)] != prefix :
				modelClass.__tablename__ = f"{prefix}{tableName}"
		if not hasattr(modelClass, '__fulltablename__') :
			hasPrefix = False
			if prefix is not None and len(prefix) :
				if modelClass.__tablename__[:len(prefix)] != prefix :
					modelClass.__fulltablename__ = f"{prefix}{modelClass.__tablename__}"
					hasPrefix = True
			if not hasPrefix :
				modelClass.__fulltablename__ = modelClass.__tablename__

		modelClass.__tablename__ = modelClass.__tablename__.lower()
		modelClass.__fulltablename__ = modelClass.__fulltablename__.lower()

	def createConnection(self):
		self.connection = psycopg2.connect(
			user=self.config["user"],
			password=self.config["password"],
			host=self.config["host"],
			port=self.config["port"],
			database=self.config["database"]
		)
		self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
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
		modelClass.__insert_column__ = ", ".join([i[0] for i in meta])
		modelClass.__insert_parameter__ = ", ".join(['%s']*len(meta))
		modelClass.__all_column__ = ", ".join([i[0] for i in modelClass.meta])
		modelClass.__all_parameter__ = ", ".join(['%s']*len(modelClass.meta))
		modelClass.__update_set_parameter__  = ", ".join(["%s=%%s"%(m[0]) for i, m in enumerate(meta)])
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
			logging.error(query)
			logging.error(parameter)
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
			logging.error(query)
			logging.error(parameter)
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
			return "SELECT COUNT(%s) AS COUNTED FROM %s%s %s"%(
				', '.join(modelClass.primary),
				self.schema,
				modelClass.__fulltablename__,
				clause
			)
		else:
			return "SELECT COUNT(%s) AS COUNTED FROM %s%s %s"%(
				modelClass.primary,
				self.schema,
				modelClass.__fulltablename__,
				clause
			)
		
	def generateSelectQuery(self, modelClass, clause, limit=None, offset=None) :
		limitClause = "" if limit is None else "LIMIT %d"%(limit)
		offsetClause = "" if offset is None else "OFFSET %d"%(offset)
		return "SELECT %s FROM %s%s %s %s %s"%(
			modelClass.__select_column__,
			self.schema,
			modelClass.__fulltablename__,
			clause, limitClause, offsetClause
		)
	
	def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		query = self.generateInsertQuery(record, isAutoID)
		value = self.getRawValue(record, isAutoID)
		self.executeWrite(query, value)
		if not isAutoID :
			if len(modelClass.children) : self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			result = self.cursor.fetchall()
			if len(result) :
				key = result[0][0]
				setattr(record, modelClass.primary, key)
				if len(modelClass.children) : self.insertChildren(record, modelClass)
				return key
		elif len(modelClass) > 0 :
			logging.warning(f"Primary key of {modelClass.__tablename__} is not auto generated. Children cannot be inserted.")
	
	def generateInsertQuery(self, record, isAutoID=True) :
		modelClass = record.__class__
		if isAutoID :
			if modelClass.__is_increment__ :
				return "INSERT INTO %s%s(%s) VALUES(%s) RETURNING %s"%(
					self.schema,
					modelClass.__fulltablename__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__,
					modelClass.primary
				)
			else :
				return "INSERT INTO %s%s(%s) VALUES(%s)"%(
					self.schema,
					modelClass.__fulltablename__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__
				)
		else :
			return "INSERT INTO %s%s(%s) VALUES(%s)"%(
				self.schema,
				modelClass.__fulltablename__,
				modelClass.__all_column__,
				modelClass.__all_parameter__
			)

	def insertMultiple(self, recordList, isAutoID=True) :
		if len(recordList) == 0 : return
		valueList = []
		modelClass = None
		for record in recordList :
			valueList.append(self.getRawValue(record, isAutoID))
			if modelClass is None :
				modelClass = record.__class__
		query = self.generateInsertMultipleQuery(modelClass, isAutoID)
		try :
			cursor = self.connection.writerCursor if self.isRoundRobin else self.cursor
			psycopg2.extras.execute_values(cursor, query, valueList)
		except Exception as error :
			logging.error(query)
			logging.error(valueList)
			self.closeConnection()
			self.connect()
			raise error
	
	def generateInsertMultipleQuery(self, modelClass, isAutoID=True) :
		if isAutoID :
			return f"INSERT INTO {self.schema}{modelClass.__fulltablename__}({modelClass.__insert_column__}) VALUES %s"
		else :
			return f"INSERT INTO {self.schema}{modelClass.__fulltablename__}({modelClass.__all_column__}) VALUES %s"

	def update(self, record) :
		modelClass = record.__class__
		value = self.getRawValue(record)
		query = self.generateUpdateQuery(record)
		self.executeWrite(query, value)
		if len(modelClass.children) : self.updateChildren(record, modelClass)
	
	def generateUpdateQuery(self, record) :
		modelClass = record.__class__
		return "UPDATE %s%s SET %s WHERE %s"%(
			self.schema,
			modelClass.__fulltablename__,
			modelClass.__update_set_parameter__,
			self.getPrimaryClause(record)
		)

	def drop(self, record) :
		self.dropChildren(record, record.__class__)
		table = record.__fulltablename__
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, self.getPrimaryClause(record))
		self.executeWrite(query)
	
	def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be dropped by ID.")
			return
		table = modelClass.__fulltablename__
		self.dropChildrenByID(ID, modelClass)
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s%s WHERE %s=%s"%(self.schema, table, modelClass.primary, ID)
		self.executeWrite(query)
	
	def dropByCondition(self, modelClass, clause) :
		table = modelClass.__fulltablename__
		parentQuery = f"SELECT {self.schema}{modelClass.primary} FROM {table} {clause}"
		for child in modelClass.children :
			childTable = child.model.__fulltablename__
			query = f"DELETE FROM {self.schema}{childTable} WHERE {child.column} IN ({parentQuery})"
			self.executeWrite(query)
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, clause)
		self.executeWrite(query)
	
	def dropChildren(self, record, modelClass) :
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {self.schema}{table} WHERE {child.column}={primary}"
			self.executeWrite(query)

	def dropChildrenByID(self, recordID, modelClass) :
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM{self.schema}{table} WHERE {child.column}={recordID}"
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
		query = [f"CREATE TABLE IF NOT EXISTS {self.schema}{model.__fulltablename__} (\n\t"]
		if len(primaryList) :
			columnList.append("PRIMARY KEY(%s)"%(",".join(primaryList)))
		if isIncremental :
			columnList.insert(0, "%s BIGSERIAL"%(model.primary))
		
		query.append(",\n\t".join(columnList))
		query.append(")")
		return " ".join(query)

	def createIndex(self, model) :
		query = self.generateIndexCheckQuery(model)
		self.cursor.execute("".join(query))
		exisitingIndex = {i[0] for i in self.cursor}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				self.executeWrite(self.generateIndexQuery(model, name))
	
	def generateIndexQuery(self, model, columnName) :
		return "CREATE INDEX IF NOT EXISTS %s%s_%s ON %s%s(%s)"%(
			f"{self.schema[:-1]}_" if len(self.schema) else "",
			model.__fulltablename__, columnName,
			self.schema, model.__fulltablename__, columnName
		)

	def getExistingTable(self) :
		self.cursor.execute(self.generateTableQuery())
		self.existingTable = {row[0] for row in self.cursor}
		return self.existingTable

	def generateTableQuery(self) :
		return "SELECT table_name FROM information_schema.tables WHERE table_schema='%s'"%(
			self.schema[:-1] if len(self.schema) else "public"
		)

	def generateIndexCheckQuery(self, model) :
		query  = ["SELECT a.attname as column "]
		query.append("FROM pg_class t, pg_class i, pg_index ix, pg_attribute a ")
		query.append("WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND ")
		query.append("a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND ")
		query.append(f"t.relkind = 'r' AND t.relname='{self.schema}{model.__fulltablename__}'")
		return "".join(query)	