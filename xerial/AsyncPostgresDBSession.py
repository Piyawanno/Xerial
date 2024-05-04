from xerial.PostgresDBSession import PostgresDBSession
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.IntegerColumn import IntegerColumn
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector
from typing import List, Dict, Any

import logging, asyncio, time, traceback

try :
	import asyncpg
except :
	logging.warning("Module asyncpg cannot be imported.")

class AsyncPostgresDBSession (PostgresDBSession, AsyncDBSessionBase) :
	def __init__(self, config) :
		AsyncDBSessionBase.__init__(self, config)
		self.schema = ""
	
	async def checkSchema(self, schema) :
		query = self.generateCheckSchema(schema)
		cursor = await self.executeRead(query, None)
		for i in cursor :
			return True
		return False
	
	async def createSchema(self, schema) :
		query = self.generateCreateSchema(schema)
		await self.executeWrite(query)

	async def dropSchema(self, schema) :
		query = self.generateDropSchema(schema)
		await self.executeWrite(query)
	
	def processClause(self, clause: str, parameter:list) -> str:
		n = 1
		p = 0
		processed = []
		cursor = -1
		while True :
			i = clause.find("?", p)
			if i < 0 :
				if p == 0 : return clause
				else : break
			processed.append(clause[p:i])
			processed.append(f"${n}")
			p = i+1
			n = n+1
			cursor = i
		if cursor == -1: return "".join(processed)
		return "".join(processed) + clause[cursor+1:]

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
		modelClass.__select_column__ = ", ".join([f'{table}.{i[0].lower()}' for i in modelClass.meta])
		modelClass.__insert_column__ = ", ".join([i[0].lower() for i in meta ])
		modelClass.__insert_record_column__ = ", ".join([f"r.{i[0].lower()}" for i in meta ])
		modelClass.__insert_column_list__ = [i[0].lower() for i in meta ]
		modelClass.__insert_parameter__ = ", ".join(["$%d"%(i+1) for i, m in enumerate(meta)])
		modelClass.__all_column__ = ", ".join([i[0].lower() for i in modelClass.meta])
		modelClass.__all_column_list__ = [i[0].lower() for i in modelClass.meta]
		modelClass.__all_parameter__ = ", ".join(["$%d"%(i+1) for i, m in enumerate(modelClass.meta)])
		modelClass.__update_set_parameter__  = ", ".join(["%s=$%d"%(m[0].lower(), i+1) for i, m in enumerate(meta) ])
		if modelClass.__is_increment__ :
			modelClass.insertMeta = [i for i in modelClass.meta if i[1] != primary]
		else :
			modelClass.insertMeta = modelClass.meta

	async def connect(self, connection=None) :
		if connection is not None :
			self.isRoundRobin = isinstance(connection, AsyncRoundRobinConnector)
			self.connection = connection
		else :
			if self.isRoundRobin :
				self.connection = AsyncRoundRobinConnector(self.config)
				await self.connection.connect(False)
			else :
				await self.createConnection()
		self.mapExecute()

	async def createConnection(self) :
		self.connection = await asyncpg.connect(
			user=self.config["user"],
			password=self.config["password"],
			host=self.config["host"],
			port=self.config["port"],
			database=self.config["database"]
		)
		self.isRoundRobin = False
		self.isOpened = True
		return self.connection
	
	async def closeConnection(self) :
		await self.connection.close()
		self.isOpened = False
	
	async def executeRoundRobinRead(self, query, parameter=None) :
		self.queryCount += 1
		connection = self.connection.getNextRead()
		try :
			if parameter is None :
				result = await connection.fetch(query)
			else :
				result = await connection.fetch(query, *parameter)
			return result
		except Exception as error :
			logging.error(query)
			logging.error(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRoundRobinWrite(self, query, parameter=None) :
		self.queryCount += 1
		connection = self.connection.writer
		try :
			if parameter is None :
				result = await connection.fetch(query)
			else :
				result = await connection.fetch(query, *parameter)
			return result
		except Exception as error :
			logging.error(query)
			logging.error(parameter)
			await self.closeConnection()
			await self.connect()
			raise error

	async def executeRegularRead(self, query, parameter=None) :
		self.queryCount += 1
		try :
			if parameter is None :
				result = await self.connection.fetch(query)
			else :
				result = await self.connection.fetch(query, *parameter)
			return result
		except Exception as error :
			logging.error(query)
			logging.error(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRegularWrite(self, query, parameter=None) :
		self.queryCount += 1
		return await self.executeRegularRead(query, parameter)

	async def insert(self, record, isAutoID=True) :
		modelClass = record.__class__
		query = self.generateInsertQuery(record, isAutoID)
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = now
		value = self.getRawValue(record, isAutoID)
		result = await self.executeWrite(query, value)
		if not isAutoID :
			if len(modelClass.children) :
				await self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			if len(result) :
				key = result[0][0]
				setattr(record, modelClass.primary, key)
				if len(modelClass.children) :
					await self.insertChildren(record, modelClass)
				return key
		elif len(modelClass) > 0 :
			logging.warning(f"Primary key of {modelClass.__table_name__} is not auto generated. Children cannot be inserted.")

	async def insertMultiple(self, recordList, isAutoID=True, isReturningID=False) :
		if len(recordList) == 0 : return
		valueList = []
		modelClass = None
		hasChildren = False
		for record in recordList :
			if modelClass is None :
				modelClass = record.__class__
				isBackup = modelClass.__backup__
				now = time.time()
				if len(modelClass.children) and not (isAutoID and isReturningID):
					hasChildren = True
					break
			if isBackup :
				record.__insert_time__ = now
				record.__update_time__ = now
			valueList.append(self.getRawValue(record, isAutoID))

		if isAutoID and isReturningID :
			return await self.insertMultipleWithID(modelClass, recordList, valueList)
		elif hasChildren :
			for record in recordList :
				await self.insert(record, isAutoID=isAutoID)
			return
		
		try :
			connection = self.connection.writer if self.isRoundRobin else self.connection
			await connection.copy_records_to_table(
				modelClass.__full_table_name__,
				records=valueList,
				columns=modelClass.__insert_column_list__ if isAutoID else modelClass.__all_column_list__,
				schema_name=self.schema[:-1] if len(self.schema) else "public"
			)
		except Exception as error :
			logging.debug(valueList)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def insertMultipleWithID(self, modelClass:type, recordList:list, valueList:list) :
		query = self.generateInsertMultipleQuery(modelClass, len(recordList))
		processed = []
		for i in valueList :
			processed.extend(i)
		fetched = await self.executeWrite(query, processed)
		result = []
		for record, raw in zip(recordList, fetched) :
			setattr(record, modelClass.primary, raw[0])
			result.append(raw[0])

		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childrenNumber = []
			accumulateChildren = []
			for record in recordList :
				childRecordList = getattr(record, child.name)
				primary = getattr(record, modelClass.primary)
				for childRecord in childRecordList :
					setattr(childRecord, child.parentColumn, primary)
				childrenNumber.append(len(childRecordList))
				accumulateChildren.extend(childRecordList)
			await self.insertMultiple(accumulateChildren, isAutoID=True, isReturningID=True)
			primary = getattr(recordList[0], modelClass.primary)
			change = childrenNumber[0]
			i, j, n = 0, 0, len(recordList)
			for childRecord in accumulateChildren :
				setattr(childRecord, child.parentColumn, primary)
				i += 1
				if i >= change and j+1 < n:
					i, j = 0, j+1
					primary = getattr(recordList[j], modelClass.primary)
					change = childrenNumber[j]
		return result
	
	def generateInsertMultipleQuery(self, modelClass, n:int, isAutoID=True) :
		if isAutoID :
			i, m = 1, len(modelClass.meta)-1
			parameter = []
			for _ in range(n) :
				parameter.append(','.join([f'${j}' for j in range(i, i+m)]))
				i += m
			return ''.join([
				f"INSERT INTO {self.schema}{modelClass.__full_table_name__}",
				f"({modelClass.__insert_column__}) VALUES (",
				'),('.join(parameter),
				f") RETURNING {modelClass.primary}"
			])
		else :
			return f"INSERT INTO {self.schema}{modelClass.__full_table_name__}({modelClass.__all_column__}) VALUES %s"

	async def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		try :
			connection = self.connection.writer if self.isRoundRobin else self.connection
			await connection.copy_records_to_table(
				modelClass.__full_table_name__,
				records=valueList,
				columns=modelClass.__all_column_list__,
				schema_name=self.schema[:-1] if len(self.schema) else "public"
			)
		except Exception as error :
			logging.debug(valueList)
			await self.closeConnection()
			await self.connect()
			raise error

	async def update(self, record) :
		modelClass = record.__class__
		if modelClass.__backup__ :
			record.__update_time__ = time.time()
		value = self.getRawValue(record)
		query = self.generateUpdateQuery(record)
		await self.executeWrite(query, value)
		if len(modelClass.children) :
			await self.updateChildren(record, modelClass)
	
	async def updateDirect(self, modelClass, raw) :
		value = self.toTuple(modelClass, raw)
		query = self.generateRawUpdateQuery(modelClass, raw)
		await self.executeWrite(query, value)

	async def drop(self, record) :
		await self.dropChildren(record, record.__class__)
		table = record.__full_table_name__
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, self.getPrimaryClause(record))
		await self.executeWrite(query)
	
	async def dropByID(self, modelClass, id) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__full_table_name__} has not primary key and cannot be dropped by ID.")
			return
		table = modelClass.__full_table_name__
		await self.dropChildrenByID(ID, modelClass)
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(id)
		query = "DELETE FROM %s%s WHERE %s=%s"%(self.schema, table, modelClass.primary, ID)
		await self.executeWrite(query)
	
	async def dropByCondition(self, modelClass, clause) :
		table = modelClass.__full_table_name__
		parentQuery = f"SELECT {modelClass.primary} FROM {self.schema}{table} WHERE {clause}"
		for child in modelClass.children :
			if not hasattr(child.model, '__full_table_name__'): continue
			childTable = child.model.__full_table_name__
			query = f"DELETE FROM {self.schema}{childTable} WHERE {child.column} IN ({parentQuery})"
			await self.executeWrite(query)
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, clause)
		await self.executeWrite(query)
	
	async def dropChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__full_table_name__
			query = f"DELETE FROM {self.schema}{table} WHERE {child.column}={primary}"
			await self.executeWrite(query)

	async def dropChildrenByID(self, recordID, modelClass) :
		self.checkLinkingMeta()
		for child in modelClass.children :
			table = child.model.__full_table_name__
			query = f"DELETE FROM{self.schema}{table} WHERE {child.column}={recordID}"
			await self.executeWrite(query)
	
	async def createTable(self) :
		if not self.checkCreateTable(): return
		await self.getExistingTable()
		for model in self.model.values() :
			if not self.checkCreateEachTable(model): continue
			self.appendCreatedTable(model)
			if hasattr(model, '__skip_create__') and model.__skip_create__ : continue
			if model.__full_table_name__ in self.existingTable :
				await self.createIndex(model)
				continue
			query = self.generateCreateTable(model)
			await self.executeWrite(query)
			await self.createIndex(model)
	
	async def createIndex(self, model) :
		if not self.checkCreateIndex(model): return
		query = self.generateIndexCheckQuery(model)
		result = await self.executeRead("".join(query))
		existingIndex = {i[0] for i in result}
		for name, column in model.meta :
			if column.isIndex and name.lower() not in existingIndex :
				query = self.generateIndexQuery(model, name)
				self.appendCreatedIndex(model, name)
				try :
					await self.executeWrite(query)
				except :
					print(f"*** ERROR BY: {query}")

			model.__generated_index__.add(name)

	async def getExistingTable(self) :
		query = self.generateTableQuery()
		result = await self.executeRead(query)
		self.existingTable = {row[0] for row in result}
		return self.existingTable

	async def getDBColumnName(self, model: type) -> List[str]:
		if len(self.schema) == 0:
			query = f"SELECT column_name FROM information_schema.columns WHERE table_name='{model.__full_table_name__}'"
		else:
			query = f"SELECT column_name FROM information_schema.columns WHERE table_schema='{self.schema[:-1]}' AND table_name='{model.__full_table_name__}'"
		result = await self.executeRead(query)
		return [i[0] for i in result]