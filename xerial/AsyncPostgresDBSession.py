from xerial.PostgresDBSession import PostgresDBSession
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.IntegerColumn import IntegerColumn
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector

import logging, asyncio
try :
	import asyncpg
except :
	logging.warning("Module asyncpg cannot be imported.")

class AsyncPostgresDBSession (PostgresDBSession, AsyncDBSessionBase) :
	def __init__(self, config) :
		AsyncDBSessionBase.__init__(self, config)
		self.schema = ""
	
	async def createSchema(self, schema) :
		query = self.generateCreateSchema(schema)
		await self.executeWrite(query)
	
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
			processed.append(f"${n}")
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
		modelClass.__select_column__ = ", ".join([i[0].lower() for i in modelClass.meta])
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
		return self.connection
	
	async def closeConnection(self) :
		await self.connection.close()
	
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
		return await self.executeRegularRead(query, parameter)
	
	async def insert(self, record, isAutoID=True) :
		modelClass = record.__class__
		query = self.generateInsertQuery(record, isAutoID)
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
			logging.warning(f"Primary key of {modelClass.__tablename__} is not auto generated. Children cannot be inserted.")

	async def insertMultiple(self, recordList, isAutoID=True, isReturningID=False) :
		if len(recordList) == 0 : return
		if isAutoID and isReturningID :
			keyList = []
			for record in recordList :
				keyList.append(await self.insert(record))
			return keyList
		valueList = []
		modelClass = None
		hasChildren = False
		for record in recordList :
			valueList.append(self.getRawValue(record, isAutoID))
			if modelClass is None :
				modelClass = record.__class__
				if len(modelClass.children) :
					hasChildren = True
					break

		if hasChildren :
			for record in recordList :
				await self.insert(record)
			return
		
		try :
			connection = self.connection.writer if self.isRoundRobin else self.connection
			await connection.copy_records_to_table(
				modelClass.__fulltablename__,
				records=valueList,
				columns=modelClass.__insert_column_list__ if isAutoID else modelClass.__all_column_list__,
				schema_name=self.schema[:-1] if len(self.schema) else "public"
			)
		except Exception as error :
			logging.debug(valueList)
			await self.closeConnection()
			await self.connect()
			raise error
	
	def generateInsertMultipleQuery(self, modelClass, isAutoID=True) :
		if isAutoID :
			return ''.join([
				f"INSERT INTO {self.schema}{modelClass.__fulltablename__}",
				f"({modelClass.__insert_column__}) (",
				f"SELECT {modelClass.__insert_record_column__} FROM ",
				f"unnest($1::{self.schema}{modelClass.__fulltablename__}[]) as r",
				f") RETURNING {modelClass.primary}"
			])
		else :
			return f"INSERT INTO {self.schema}{modelClass.__fulltablename__}({modelClass.__all_column__}) VALUES %s"


	async def update(self, record) :
		modelClass = record.__class__
		value = self.getRawValue(record)
		query = self.generateUpdateQuery(record)
		await self.executeWrite(query, value)
		if len(modelClass.children) :
			await self.updateChildren(record, modelClass)
	
	async def drop(self, record) :
		await self.dropChildren(record, record.__class__)
		table = record.__fulltablename__
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, self.getPrimaryClause(record))
		await self.executeWrite(query)
	
	async def dropByID(self, modelClass, id) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be dropped by ID.")
			return
		table = modelClass.__fulltablename__
		await self.dropChildrenByID(ID, modelClass)
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(id)
		query = "DELETE FROM %s%s WHERE %s=%s"%(self.schema, table, modelClass.primary, ID)
		await self.executeWrite(query)
	
	async def dropByCondition(self, modelClass, clause) :
		table = modelClass.__fulltablename__
		parentQuery = f"SELECT {modelClass.primary} FROM {self.schema}{table} {clause}"
		for child in modelClass.children :
			childTable = child.model.__fulltablename__
			query = f"DELETE FROM {self.schema}{childTable} WHERE {child.column} IN ({parentQuery})"
			await self.executeWrite(query)
		query = "DELETE FROM %s%s WHERE %s"%(self.schema, table, clause)
		await self.executeWrite(query)
	
	async def dropChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {self.schema}{table} WHERE {child.column}={primary}"
			await self.executeWrite(query)

	async def dropChildrenByID(self, recordID, modelClass) :
		self.checkLinkingMeta()
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM{self.schema}{table} WHERE {child.column}={recordID}"
			await self.executeWrite(query)
	
	async def createTable(self) :
		await self.getExistingTable()
		for model in self.model.values() :
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__fulltablename__ in self.existingTable :
				await self.createIndex(model)
				continue
			query = self.generateCreateTable(model)
			await self.executeWrite(query)
			await self.createIndex(model)
	
	async def createIndex(self, model) :
		query = self.generateIndexCheckQuery(model)
		result = await self.executeRead("".join(query))
		exisitingIndex = {i[0] for i in result}
		for name, column in model.meta :
			if column.isIndex and name.lower() not in exisitingIndex :
				await self.executeWrite(self.generateIndexQuery(model, name))

	async def getExistingTable(self) :
		query = self.generateTableQuery()
		result = await self.executeRead(query)
		self.existingTable = {row[0] for row in result}
		return self.existingTable

	