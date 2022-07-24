from multiprocessing import connection
from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector
from xerial.IntegerColumn import IntegerColumn

import logging, traceback

try :
	import aiosqlite
except :
	logging.warning("Module aiomysql cannot be imported.")

class AsyncSQLiteDBSession (SQLiteDBSession, AsyncDBSessionBase) :
	async def createConnection(self):
		self.connection = await aiosqlite.connect(
			self.config["database"],
			isolation_level=None,
			check_same_thread=False
		)
	
	async def closeConnection(self) :
		await self.connection.close()
	

	async def executeRoundRobinRead(self, query, parameter=None) :
		self.queryCount += 1
		connection = self.connection.getNextRead()
		try :
			if parameter is None :
				cursor = await connection.execute(query)
			else :
				cursor = await connection.execute(query, parameter)
			return await cursor.fetchall()
		except Exception as error :
			logging.debug(query)
			logging.debug(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRoundRobinWrite(self, query, parameter=None) :
		self.queryCount += 1
		connection = self.connection.writer
		try :
			if parameter is None :
				cursor = await connection.execute(query)
			else :
				cursor = await connection.execute(query, parameter)
			return cursor
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
				cursor = await self.connection.execute(query)
			else :
				cursor = await self.connection.execute(query, parameter)
			return await cursor.fetchall()
		except Exception as error :
			logging.debug(query)
			logging.debug(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def executeRegularWrite(self, query, parameter=None):
		self.queryCount += 1
		try :
			if parameter is None :
				cursor = await self.connection.execute(query)
			else :
				cursor = await self.connection.execute(query, parameter)
			return cursor
		except Exception as error :
			logging.debug(query)
			logging.debug(parameter)
			await self.closeConnection()
			await self.connect()
			raise error

	async def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		query = self.generateInsertQuery(record, isAutoID)
		value = self.getRawValue(record, isAutoID)
		cursor = await self.executeWrite(query, value)
		if not isAutoID :
			if len(modelClass.children) : await self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			setattr(record, modelClass.primary, cursor.lastrowid)
			if len(modelClass.children) : await self.insertChildren(record, modelClass)
			return cursor.lastrowid
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

		query = self.generateInsertQuery(record, isAutoID)
		try :
			connection = self.connection.writer if self.isRoundRobin else self.connection
			await connection.executemany(query, valueList)
		except Exception as error :
			logging.debug(query)
			logging.debug(valueList)
			self.closeConnection()
			self.connect()
			raise error
	
	async def update(self, record) :
		modelClass = record.__class__
		value = self.getRawValue(record)
		query = self.generateUpdateQuery(record)
		await self.executeWrite(query, value)
		if len(modelClass.children) : await self.updateChildren(record, modelClass)
	
	async def drop(self, record) :
		await self.dropChildren(record, record.__class__)
		table = record.__fulltablename__
		query = "DELETE FROM %s WHERE %s"%(table, self.getPrimaryClause(record))
		await self.executeWrite(query)
	
	async def dropByID(self, modelClass, ID) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be dropped by ID.")
			return
		await self.dropChildrenByID(ID, modelClass)
		table = modelClass.__fulltablename__
		meta = modelClass.primaryMeta
		ID = meta.setValueToDB(ID)
		query = "DELETE FROM %s WHERE %s=%s"%(table, modelClass.primary, ID)
		await self.executeWrite(query)
	
	async def dropByCondition(self, modelClass, clause) :
		table = modelClass.__fulltablename__
		parentQuery = f"SELECT {modelClass.primary} FROM {table} {clause}"
		for child in modelClass.children :
			childTable = child.model.__fulltablename__
			query = f"DELETE FROM {childTable} WHERE {child.column} IN ({parentQuery})"
			await self.executeWrite(query)
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
		query = self.generateIndexCheckQuery(model)
		cursor = await self.executeRead(query)
		exisitingIndex = {i[0] for i in cursor}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				await self.executeWrite(self.generateIndexQuery(model, name))
	
	async def getExistingTable(self) :
		result = await self.executeRead(self.generateTableQuery())
		self.existingTable = {row[0] for row in result}
		return self.existingTable
	