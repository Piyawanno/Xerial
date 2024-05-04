from xerial.DBSessionBase import DBSessionBase, PrimaryDataError
from xerial.IntegerColumn import IntegerColumn
from packaging.version import Version
from typing import Set, List

import logging, time

try :
	import psycopg2
	import psycopg2.extras
except :
	logging.warning("Module psycopg2 cannot be imported.")

# NOTE Since PostgreSQL can use schema, if the cached state is stored
# in the model class, error can occurs. Hence, the the cached state
# will explicitly stored.
__SCHEMA_TABLE_CHECK__ = {}
__SCHEMA_INDEX_CHECK__ = {}

class PostgresDBSession (DBSessionBase) :
	def __init__(self, config) :
		DBSessionBase.__init__(self, config)
		self.schema = ""
		self.schemaName = ""
	
	def setSchema(self, schema) :
		self.schema = f"{schema.lower()}."
		self.schemaName = schema
	
	def unsetSchema(self) :
		self.schema = ""
	
	def checkSchema(self, schema) :
		query = self.generateCheckSchema(schema)
		cursor = self.executeRead(query, None)
		for i in cursor :
			return True
		return False
	
	def createSchema(self, schema) :
		query = self.generateCreateSchema(schema)
		self.executeWrite(query)
	
	def generateCreateSchema(self, schema) :
		return f"CREATE SCHEMA IF NOT EXISTS {schema.lower()}"
	
	def dropSchema(self, schema):
		query = self.generateDropSchema(schema)
		self.executeWrite(query)
	
	def generateDropSchema(self, schema) :
		return f"DROP SCHEMA IF EXISTS {schema.lower()} CASCADE"
	
	def generateCheckSchema(self, schema) :
		return f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';"
	
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
		self.isOpened = True
	
	def closeConnection(self) :
		self.connection.close()
		self.isOpened = False
	
	def processClause(self, clause: str, parameter: list) -> str:
		return clause.replace("?", "%s")

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
		print(modelClass)
		modelClass.__select_column__ = ", ".join([f'{table}{i[0]}' for i in modelClass.meta])
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
				modelClass.__full_table_name__,
				clause
			)
		else:
			return "SELECT COUNT(%s) AS COUNTED FROM %s%s %s"%(
				modelClass.primary,
				self.schema,
				modelClass.__full_table_name__,
				clause
			)
		
	def generateSelectQuery(self, modelClass, clause, limit=None, offset=None) :
		limitClause = "" if limit is None else "LIMIT %d"%(limit)
		offsetClause = "" if offset is None else "OFFSET %d"%(offset)
		return "SELECT %s FROM %s%s %s %s %s"%(
			modelClass.__select_column__,
			self.schema,
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
		query = self.generateInsertQuery(record, isAutoID)
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = -1.0
		value = self.getRawValue(record, isAutoID)
		self.executeWrite(query, value)
		if not isAutoID :
			if len(modelClass.children) :
				self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			result = self.cursor.fetchall()
			if len(result) :
				key = result[0][0]
				setattr(record, modelClass.primary, key)
				if len(modelClass.children) :
					self.insertChildren(record, modelClass)
				return key
		elif len(modelClass) > 0 :
			logging.warning(f"Primary key of {modelClass.__table_name__} is not auto generated. Children cannot be inserted.")
	
	def generateInsertQuery(self, record, isAutoID=True) :
		modelClass = record.__class__
		if isAutoID :
			if modelClass.__is_increment__ :
				return "INSERT INTO %s%s(%s) VALUES(%s) RETURNING %s"%(
					self.schema,
					modelClass.__full_table_name__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__,
					modelClass.primary
				)
			else :
				return "INSERT INTO %s%s(%s) VALUES(%s)"%(
					self.schema,
					modelClass.__full_table_name__,
					modelClass.__insert_column__,
					modelClass.__insert_parameter__
				)
		else :
			return "INSERT INTO %s%s(%s) VALUES(%s)"%(
				self.schema,
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
	
	def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		query = self.generateInsertMultipleQuery(modelClass, isAutoID=False)
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
			return f"INSERT INTO {self.schema}{modelClass.__full_table_name__}({modelClass.__insert_column__}) VALUES %s"
		else :
			return f"INSERT INTO {self.schema}{modelClass.__full_table_name__}({modelClass.__all_column__}) VALUES %s"

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
		return "UPDATE %s%s SET %s WHERE %s"%(
			self.schema,
			modelClass.__full_table_name__,
			modelClass.__update_set_parameter__,
			self.getPrimaryClause(record)
		)
	
	def generateRawUpdateQuery(self, modelClass, raw) :
		return "UPDATE %s%s SET %s WHERE %s"%(
			self.schema,
			modelClass.__full_table_name__,
			modelClass.__update_set_parameter__,
			self.getRawPrimaryClause(modelClass, raw)
		)

	def drop(self, record) :
		self.dropChildren(record, record.__class__)
		table = record.__full_table_name__
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, self.getPrimaryClause(record))
		self.executeWrite(query)
	
	def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__full_table_name__} has not primary key and cannot be dropped by ID.")
			return
		table = modelClass.__full_table_name__
		self.dropChildrenByID(ID, modelClass)
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s%s WHERE %s=%s"%(self.schema, table, modelClass.primary, ID)
		self.executeWrite(query)
	
	def dropByCondition(self, modelClass, clause) :
		table = modelClass.__full_table_name__
		parentQuery = f"SELECT {self.schema}{modelClass.primary} FROM {table} {clause}"
		for child in modelClass.children :
			childTable = child.model.__full_table_name__
			query = f"DELETE FROM {self.schema}{childTable} WHERE {child.column} IN ({parentQuery})"
			self.executeWrite(query)
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, clause)
		self.executeWrite(query)
	
	def dropChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__full_table_name__
			query = f"DELETE FROM {self.schema}{table} WHERE {child.column}={primary}"
			self.executeWrite(query)

	def dropChildrenByID(self, recordID, modelClass) :
		self.checkLinkingMeta(modelClass)
		for child in modelClass.children :
			table = child.model.__full_table_name__
			query = f"DELETE FROM{self.schema}{table} WHERE {child.column}={recordID}"
			self.executeWrite(query)
	
	def createTable(self) :
		if not self.checkCreateTable(): return
		self.getExistingTable()
		for model in self.model.values() :
			if not self.checkCreateEachTable(model) : continue
			self.appendCreatedTable(model)
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__full_table_name__ in self.existingTable :
				self.createIndex(model)
				continue
			query = self.generateCreateTable(model)
			self.executeWrite(query)
			self.createIndex(model)
	
	def generateModification(self, modelClass, currentVersion) :
		currentVersion = Version(currentVersion)
		queryList = []
		record = modelClass.__new__(modelClass)
		record.modify()
		if not hasattr(modelClass, '__modification__') : return queryList
		for i in modelClass.__modification__ :
			if i.version > currentVersion :
				i.setSchema(self.schema)
				queryList.append((i.version, i.generateQuery()))
		return queryList
	
	def generateCreateTable(self, model) :
		columnList = []
		isIncremental = model.__is_increment__
		isPrimaryList = hasattr(model, 'primaryMeta') and isinstance(model.primaryMeta, list)
		hasPrimary = False
		primaryList = []
		for name, column in model.meta :
			# if not (isIncremental and column.isPrimary) :
			primary = ""
			if column.isPrimary :
				if isPrimaryList : primaryList.append(name)
				else : primary = "PRIMARY KEY"
				hasPrimary = True
			notNull = "NOT NULL" if column.isNotNull else ""
			isDefault = hasattr(column, 'default') and column.default is not None
			defaultValue = column.default() if callable(column.default) else column.default
			default = "DEFAULT %s"%(column.setValueToDB(defaultValue)) if isDefault else ""
			columnList.append(f"{name} {column.getDBDataType()} {primary} {default} {notNull}")
		query = [f"CREATE TABLE IF NOT EXISTS {self.schema}{model.__full_table_name__} (\n\t"]
		if len(primaryList) :
			columnList.append("PRIMARY KEY(%s)"%(",".join(primaryList)))
		if not hasPrimary and isIncremental :
			columnList.insert(0, "%s BIGSERIAL"%(model.primary))
		
		query.append(",\n\t".join(columnList))
		query.append(")")
		return " ".join(query)

	def createIndex(self, model) :
		if not self.checkCreateIndex(model): return
		query = self.generateIndexCheckQuery(model)
		self.cursor.execute("".join(query))
		existingIndex = {i[0] for i in self.cursor}
		for name, column in model.meta :
			if column.isIndex and name not in existingIndex :
				self.appendCreatedIndex(model, name)
				query = self.generateIndexQuery(model, name)
				try:
					self.executeWrite(query)
				except:
					print(f"*** ERROR BY: {query}")
				
	
	def generateIndexQuery(self, model, columnName) :
		return "CREATE INDEX IF NOT EXISTS %s%s_%s ON %s%s(%s)"%(
			f"{self.schema[:-1]}_" if len(self.schema) else "",
			model.__full_table_name__, columnName,
			self.schema, model.__full_table_name__, columnName
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
		query.append(f"t.relkind = 'r' AND t.relname='{self.schema}{model.__full_table_name__}'")
		return "".join(query)
	
	def generateResetID(self, modelClass:type) -> str :
		return f"ALTER SEQUENCE {self.schema}{modelClass.__full_table_name__} RESTART ?;"

	def generateDropTable(self, modelClass:type) -> str :
		return f"DROP TABLE {modelClass.__full_table_name__} CASCADE"
	
	def checkCreateTable(self) -> bool:
		if self.schema is None or len(self.schema) == 0:
			return DBSessionBase.checkCreateTable(self)
		createdSet: Set[str] = __SCHEMA_TABLE_CHECK__.get(self.schema, set())
		if len(createdSet) == 0: __SCHEMA_TABLE_CHECK__[self.schema] = createdSet
		toCreate = False
		for model in self.model.values() :
			if model.__name__ not in createdSet:
				createdSet.add(model.__name__)
				toCreate = True
		return toCreate
	
	def checkCreateEachTable(self, model: type) -> bool:
		if self.schema is None or len(self.schema) == 0:
			return not (hasattr(model, '__is_created__') and model.__is_created__ and model.__full_table_name__ in self.existingTable)
		createdSet: Set[str] = __SCHEMA_TABLE_CHECK__.get(self.schema, set())
		if len(createdSet) == 0: __SCHEMA_TABLE_CHECK__[self.schema] = createdSet
		return model.__name__ in createdSet
	
	def appendCreatedTable(self, model: type):
		if self.schema is None or len(self.schema) == 0: return
		createdSet: Set[str] = __SCHEMA_TABLE_CHECK__.get(self.schema, set())
		if len(createdSet) == 0: __SCHEMA_TABLE_CHECK__[self.schema] = createdSet
		createdSet.add(model.__name__)

	def resetCheckTable(self) :
		pass
	
	def checkCreateIndex(self, model: type) -> bool:
		if self.schema is None or len(self.schema) == 0:
			return DBSessionBase.checkCreateIndex(self, model)
		indexSet = self.getIndexSet(model)
		for name, column in model.meta:
			if name not in indexSet: return False
		return True

	def appendCreatedIndex(self, model: type, columnName: str):
		if self.schema is None or len(self.schema) == 0: return
		indexSet = self.getIndexSet(model)
		indexSet.add(columnName)
	
	def getIndexSet(self, model: type) -> Set[str] :
		tableMap = __SCHEMA_INDEX_CHECK__.get(self.schema, {})
		if len(tableMap) == 0: __SCHEMA_INDEX_CHECK__[self.schema] = tableMap
		indexSet = tableMap.get(model.__name__, None)
		# NOTE It cannot check length, some table has no index.
		# Otherwise, length will be checked by every call.
		if indexSet is None:
			indexSet = set()
			tableMap[model.__name__] = indexSet
		return indexSet
	
	def getDBColumnName(self, model: type) -> List[str]:
		if len(self.schema) == 0:
			query = f"SELECT column_name FROM information_schema.columns WHERE table_name='{model.__full_table_name__}'"
		else:
			query = f"SELECT column_name FROM information_schema.columns WHERE table_schema='{self.schema[:-1]}' AND table_name='{model.__full_table_name__}'"
		result = self.executeRead(query)
		return [i[0] for i in result]