from xerial.OracleDBSession import OracleDBSession
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector

import logging, traceback, time

try :
	import cx_Oracle_async
	import cx_Oracle
except :
	logging.warning("Module cx_Oracle_async cannot be imported.")

class AsyncOracleDBSession (OracleDBSession, AsyncDBSessionBase) :
	async def createConnection(self):
		self.pool = await cx_Oracle_async.create_pool(
			host=self.config['host'],
			port=self.config['port'],
			user=self.config['user'],
			password=self.config['password'],
			service_name=self.config['domain'],
		)
		self.connection = await self.pool.acquire()
		self.connection.autocommit = True
		self.cursor = await self.connection.cursor()
		self.isOpened = True

	async def closeConnection(self) :
		del self.cursor
		del self.connection
		self.isOpened = False

	async def executeRoundRobinRead(self, query, parameter=None) :
		self.queryCount += 1
		cursor = self.connection.getNextReadCursor()
		try :
			if parameter is None :
				await cursor.execute(query)
			else :
				await cursor.execute(query, parameter)
			return await cursor.fetchall()
		except Exception as error :
			logging.error(query)
			logging.error(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRoundRobinWrite(self, query, parameter=None) :
		self.queryCount += 1
		cursor = self.connection.writerCursor
		try :
			if parameter is None :
				await cursor.execute(query)
			else :
				await cursor.execute(query, parameter)
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
				await self.cursor.execute(query)
			else :
				await self.cursor.execute(query, parameter)
			return await self.cursor.fetchall()
		except Exception as error :
			logging.error(query)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRegularWrite(self, query, parameter=None):
		self.queryCount += 1
		try :
			if parameter is None :
				await self.cursor.execute(query)
			else :
				await self.cursor.execute(query, parameter)
		except Exception as error :
			logging.error(query)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		query = self.generateInsert(modelClass, isAutoID)
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = now
		parameter = self.getRawValue(record, isAutoID)
		if modelClass.__insert_parameter__ :
			insertedID = self.cursor._cursor.var(cx_Oracle.NUMBER)
			parameter.append(insertedID)
		await self.executeWrite(query, parameter)
		if not isAutoID :
			if len(modelClass.children) :
				await self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			lastRow = insertedID.values[0][0]
			setattr(record, modelClass.primary, lastRow)
			if len(modelClass.children) :
				await self.insertChildren(record, modelClass)
			return lastRow
		elif len(modelClass) > 0 :
			logging.warning(f"Primary key of {modelClass.__table_name__} is not auto generated. Children cannot be inserted.")
	
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
			if modelClass is None :
				modelClass = record.__class__
				query = self.generateInsert(modelClass, isAutoID, isMultiple=True)
				isBackup = modelClass.__backup__
				now = time.time()
				if len(modelClass.children) :
					hasChildren = True
					break
			if isBackup :
				record.__insert_time__ = now
				record.__update_time__ = now
			valueList.append(self.getRawValue(record, isAutoID))
			
		if hasChildren :
			for record in recordList :
				await self.insert(record)
			return

		query = self.generateInsert(modelClass, isAutoID, isMultiple=True)
		for value in valueList :
			await self.executeWrite(query, value)
	
	async def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		query = self.generateInsert(modelClass, isAutoID=False, isMultiple=True)
		for value in valueList :
			await self.executeWrite(query, value)
	
	async def update(self, record) :
		modelClass = record.__class__
		if modelClass.__backup__ :
			record.__update_time__ = time.time()
		value = self.getRawValue(record)
		await self.executeWrite(self.generateUpdate(record), value)
		if len(modelClass.children) :
			await self.updateChildren(record, modelClass)
	
	async def updateDirect(self, modelClass, raw) :
		value = self.toTuple(modelClass, raw)
		query = self.generateRawUpdate(modelClass, raw)
		await self.executeWrite(query, value)
	
	async def drop(self, record) :
		await self.dropChildren(record, record.__class__)
		table = record.__full_table_name__
		query = "DELETE FROM %s WHERE %s"%(table, self.getPrimaryClause(record))
		await self.executeWrite(query)
	
	async def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__full_table_name__} has not primary key and cannot be dropped by ID.")
			return
		await self.dropChildrenByID(ID, modelClass)
		table = modelClass.__full_table_name__
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s WHERE %s=%s"%(table, modelClass.primary, ID)
		await self.executeWrite(query)
	
	async def dropByCondition(self, modelClass, clause) :
		table = modelClass.__full_table_name__
		parentQuery = f"SELECT {modelClass.primary} FROM {table} {clause}"
		for child in modelClass.children :
			childTable = child.model.__full_table_name__
			query = f"DELETE FROM {childTable} WHERE {child.column} IN ({parentQuery})"
			await self.executeWrite(query)
		query = "DELETE FROM %s WHERE %s"%(table, clause)
		await self.executeWrite(query)
	
	async def createTable(self) :
		await self.getExistingTable()
		for model in self.model.values() :
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__table_name__.upper() in self.existingTable : continue
			self.generateCreatTable(model)
			query = self.generateCreatTable(model)
			logging.info(f"Creating Table {model.__table_name__}")
			await self.executeWrite(query)
		await self.getExistingTable()

		for model in self.model.values() :
			if hasattr(model, '__skip_create__') and getattr(model, '__skip_create__') : continue
			if model.__table_name__.upper() in self.existingTable :
				await self.createIndex(model)
	
	async def createIndex(self, model) :
		result = await self.executeRead(self.generateIndexQuery(model))
		existingIndex =  {i[0].upper() for i in result}
		for name, column in model.meta :
			name = name.upper()
			if column.isIndex and name not in existingIndex:
				await self.executeWrite(self.generateCreateIndex(model, name))
	
	async def getExistingTable(self) :
		result = await self.executeRead(self.generateCheckTable())
		self.owner = {row[0]:row[1] for row in result}
		self.existingTable = list(self.owner.keys())
		for model in self.model.values() :
			tableName = model.__table_name__.upper()
			owner = self.owner.get(tableName)
			if owner is not None :
				model.__full_table_name__ = f"{owner}.{tableName}"
			else :
				model.__full_table_name__ = tableName
		return self.existingTable