from xerial.MSSQLDBSession import MSSQLDBSession
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector
from xerial.IntegerColumn import IntegerColumn

import logging, traceback

try :
	import aiomysql
except :
	logging.warning("Module aiomysql cannot be imported.")

class AsyncMariaDBSession (MSSQLDBSession, AsyncDBSessionBase) :
	async def createConnection(self):
		self.connection = await aiomysql.connect(
			host=self.config['host'],
			port=self.config['port'],
			user=self.config['user'],
			password=self.config['password'],
			db=self.config['database'],
		)
		self.cursor = await self.connection.cursor()

	async def closeConnection(self) :
		await self.cursor.close()
		self.connection.close()
	
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
			logging.debug(query)
			logging.debug(parameter)
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
			return await cursor.fetchall()
		except Exception as error :
			logging.debug(query)
			logging.debug(parameter)
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
			logging.error(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRegularWrite(self, query, parameter=None):
		return await self.executeRead(query, parameter)

	async def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		value = self.getRawValue(record, isAutoID)
		query = self.generateInsert(modelClass)
		cursor = await self.executeWrite(query, value)
		if modelClass.__is_increment__ :
			setattr(record, modelClass.primary, self.cursor.lastrowid)
			return cursor.lastrowid
	
	async def insertMultiple(self, recordList, isAutoID=True) :
		if len(recordList) == 0 : return
		valueList = []
		modelClass = None
		for record in recordList :
			valueList.append(tuple(self.getRawValue(record, isAutoID)))
			modelClass = record.__class__
		
		query = self.generateInsert(modelClass, isAutoID)
		try :
			cursor = self.connection.writeCursor if self.isRoundRobin else self.cursor
			await cursor.executemany(query, valueList)
		except Exception as error :
			print(query)
			logging.debug(query)
			logging.debug(valueList)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def update(self, record) :
		value = self.getRawValue(record)
		modelClass = record.__class__
		query = self.generateUpdate(modelClass)
		await self.executeWrite(query, value)
	
	async def drop(self, record) :
		table = record.__fulltablename__
		query = "DELETE FROM %s WHERE %s"%(table, self.getPrimaryClause(record))
		await self.executeWrite(query)
	
	async def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be dropped by ID.")
			return
		table = modelClass.__fulltablename__
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s WHERE %s=%s"%(table, modelClass.primary, ID)
		await self.executeWrite(query)
	
	async def dropByCondition(self, modelClass, clause) :
		table = modelClass.__fulltablename__
		query = "DELETE FROM %s WHERE %s"%(table, clause)
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
		result = await self.executeRead("SHOW INDEX FROM %s"%(model.__fulltablename__))
		exisitingIndex = {i[4] for i in result}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				await self.executeWrite("CREATE INDEX %s_%s ON %s(%s)"%(model.__fulltablename__, name, model.__fulltablename__, name))
	
	async def getExistingTable(self) :
		result = await self.executeRead("SHOW TABLES")
		self.existingTable = {row[0] for row in result}
		return self.existingTable
	