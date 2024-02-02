from xerial.MariaDBSession import MariaDBSession
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector
from xerial.IntegerColumn import IntegerColumn
from typing import List, Dict, Any
from datetime import datetime

import logging, traceback, time

try :
	import aiomysql
except :
	logging.warning("Module aiomysql cannot be imported.")

class AsyncMariaDBSession (MariaDBSession, AsyncDBSessionBase) :
	async def createConnection(self):
		self.connection = await aiomysql.connect(
			host=self.config['host'],
			port=self.config['port'],
			user=self.config['user'],
			password=self.config['password'],
			db=self.config['database'],
		)
		self.cursor = await self.connection.cursor()
		self.isOpened = True

	async def closeConnection(self) :
		try :
			await self.cursor.close()
			self.connection.close()
			self.isOpened = False
		except :
			print(">>> Error by closing MariaDB connection.")
	
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
		modelClass.__select_column__ = ", ".join([f'{table}.{i[0]}' for i in modelClass.meta])
		modelClass.__insert_column__ = ", ".join([i[0] for i in meta])
		modelClass.__insert_parameter__ = ", ".join(['%s']*len(meta))
		modelClass.__all_column__ = ", ".join([i[0] for i in modelClass.meta])
		modelClass.__all_parameter__ = ", ".join(['%s']*len(modelClass.meta))
		modelClass.__update_set_parameter__  = ", ".join(["%s=%%s"%(m[0]) for i, m in enumerate(meta)])
		if modelClass.__is_increment__ :
			modelClass.insertMeta = [i for i in modelClass.meta if i[1] != primary]
		else :
			modelClass.insertMeta = modelClass.meta
	
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
		self.queryCount += 1
		try :
			if parameter is None :
				await self.cursor.execute(query)
			else :
				await self.cursor.execute(query, parameter)
			return self.cursor
		except Exception as error :
			logging.error(query)
			logging.error(parameter)
			await self.closeConnection()
			await self.connect()
			raise error
	
	async def selectRaw(self, query:str) -> List[Dict[str, Any]] :
		cursor = await self.connection.cursor(aiomysql.DictCursor)
		await cursor.execute(query)
		fetched = await cursor.fetchall()
		return self.convertRaw(fetched)

	async def insert(self, record, isAutoID=True):
		modelClass = record.__class__
		if modelClass.__backup__ :
			now = time.time()
			record.__insert_time__ = now
			record.__update_time__ = now
		value = self.getRawValue(record, isAutoID)
		query = self.generateInsert(modelClass)
		cursor = await self.executeWrite(query, value)
		if not isAutoID :
			if len(modelClass.children) :
				await self.insertChildren(record, modelClass)
		elif modelClass.__is_increment__ :
			setattr(record, modelClass.primary, self.cursor.lastrowid)
			if len(modelClass.children) :
				await self.insertChildren(record, modelClass)
			return cursor.lastrowid
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
	
	async def insertMultipleDirect(self, modelClass, rawList) :
		valueList = [self.toTuple(modelClass, raw) for raw in rawList]
		query = self.generateInsert(modelClass, isAutoID=False)
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
		modelClass = record.__class__
		if modelClass.__backup__ :
			record.__update_time__ = time.time()
		value = self.getRawValue(record)
		query = self.generateUpdate(record)
		await self.executeWrite(query, value)
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
			if model.__full_table_name__ in self.existingTable :
				await self.createIndex(model)
				continue
			query = self.generateCreateTable(model)
			await self.executeWrite(query)
			await self.createIndex(model)
	
	async def createIndex(self, model) :
		result = await self.executeRead("SHOW INDEX FROM %s"%(model.__full_table_name__))
		exisitingIndex = {i[4] for i in result}
		for name, column in model.meta :
			if column.isIndex and name not in exisitingIndex :
				await self.executeWrite("CREATE INDEX %s_%s ON %s(%s)"%(model.__full_table_name__, name, model.__full_table_name__, name))
	
	async def getExistingTable(self) :
		result = await self.executeRead("SHOW TABLES")
		self.existingTable = {row[0] for row in result}
		return self.existingTable
	