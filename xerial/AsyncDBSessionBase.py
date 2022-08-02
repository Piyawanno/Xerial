from xerial.DBSessionBase import DBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector

import logging

class AsyncDBSessionBase (DBSessionBase) :
	async def checkModification(self, modelClass, currentVersion) :
		modificationList = self.generateModification(modelClass, currentVersion)
		lastVersion = currentVersion
		for version, queryList in modificationList :
			lastVersion = version
			for query in queryList :
				try :
					await self.executeWrite(query)
				except :
					logging.error(f"Error by modify {modelClass.__name__} {query}")
		return lastVersion

	async def connect(self, connection=None) :
		if connection is not None :
			self.isRoundRobin = isinstance(connection, AsyncRoundRobinConnector)
			self.connection = connection
			self.cursor = self.connection.cursor()
		else :
			if self.isRoundRobin :
				self.connection = AsyncRoundRobinConnector(self.config)
				await self.connection.connect(True)
			else :
				await self.createConnection()
	
	async def count(self, modelClass:type, clause:str, parameter:list=None) -> int :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateCountQuery(modelClass, clause)
		cursor = await self.executeRead(query, parameter)
		for i in cursor :
			return i[0]

	async def select(self, modelClass:type, clause:str, isRelated:bool=False, limit:int=None, offset:int=None, parameter:list=None) -> list:
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = await self.executeRead(query, parameter)
		result = []
		for row in cursor :
			record = modelClass()
			i = 0
			for columnName, column in modelClass.meta :
				setattr(record, columnName, column.processValue(row[i]))
				i += 1
			result.append(record)
		if isRelated :
			await self.selectRelated(modelClass, result)
			await self.selectChildren(modelClass, result)
		return result
	
	async def selectTranspose(self, modelClass:type, clause:str, isRelated:bool=False, limit:int=None, offset:int=None, parameter:list=None) -> dict :
		recordList = await self.select(modelClass, clause, isRelated, limit, offset, parameter)
		result = {}
		for name, column in modelClass.meta :
			result[name] = []
		for record in recordList :
			data = record.toDict()
			for name, column in modelClass.meta :
				result[name].append(data[name])
		return result
	
	async def selectRelated(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		self.checkLinkingMeta(modelClass)
		isMapper = modelClass.__is_mapper__
		for foreignKey in modelClass.foreignKey :
			keyList = {str(getattr(i, foreignKey.name)) for i in recordList}
			clause = "WHERE %s IN(%s)"%(foreignKey.column, ",".join(list(keyList)))
			related = await self.select(foreignKey.model, clause, isMapper)
			relatedMap = {getattr(i, foreignKey.column):i for i in related}
			for record in recordList :
				value = getattr(record, foreignKey.name)
				setattr(record, foreignKey.name, relatedMap.get(value, value))
	
	async def selectChildren(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		self.checkLinkingMeta(modelClass)
		primary = modelClass.primary
		keyList = [str(getattr(i, primary)) for i in recordList]
		joined = ','.join(keyList)
		childrenMap = {}
		childrenFlattedMap = {}
		for child in modelClass.children :
			clause = f"WHERE {child.column} IN ({joined})"
			childRecord = await self.select(child.model, clause, False)
			childrenFlattedMap[child.name] = childRecord
			columnMap = {}
			childrenMap[child.name] = columnMap
			for record in childRecord :
				parent = getattr(record, child.column)
				childrenList = columnMap.get(parent, [])
				if len(childrenList) == 0 : columnMap[parent] = childrenList
				childrenList.append(record)
		
		for child in modelClass.children :
			if not child.model.__is_mapper__ : continue
			childRecordList = childrenFlattedMap[child.name]

			for foreignKey in child.model.foreignKey :
				if foreignKey.model == modelClass : continue
				keyList = {str(getattr(i, foreignKey.name)) for i in childRecordList}
				joined = ",".join(list(keyList))
				linkedList = await self.select(foreignKey.model, f"WHERE {foreignKey.column} IN ({joined})", False)
				linkedMap = {getattr(i, foreignKey.model.primary):i for i in linkedList}
				for childRecord in childRecordList :
					key = getattr(childRecord, foreignKey.name)
					setattr(childRecord, foreignKey.name, linkedMap.get(key, None))
		
		for child in modelClass.children :
			for record in recordList :
				primary = getattr(record, modelClass.primary)
				setattr(record, child.name, childrenMap[child.name].get(primary, []))

	async def insertChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if len(childRecordList) == 0 : continue
			if not isinstance(childRecordList, list) : continue
			for childRecord in childRecordList :
				setattr(childRecord, child.column, primary)
			await self.insertMultiple(childRecordList)
	
	async def updateChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if len(childRecordList) == 0 : continue
			if not isinstance(childRecordList, list) : continue
			insertList = []
			for childRecord in childRecordList :
				childID = getattr(childRecord, child.model.primary, None)
				if childID is not None :
					await self.update(childRecord)
				else :
					insertList.append(childRecord)
					setattr(childRecord, child.column, primary)
			await self.insertMultiple(insertList)
	
	async def dropChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {table} WHERE {child.column}={primary}"
			await self.executeWrite(query)

	async def dropChildrenByID(self, recordID, modelClass) :
		self.checkLinkingMeta(modelClass)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {table} WHERE {child.column}={recordID}"
			await self.executeWrite(query)

	async def createConnection(self) :
		pass
	
	async def closeConnection(self) :
		pass
	
	async def executeRead(self, query, parameter=None) :
		pass
	
	async def executeWrite(self, query, parameter=None) :
		pass
	
	async def insert(self, record, isAutoID=True) :
		pass
	
	async def insertMultiple(self, recordList, isAutoID=True, isReturningID=False) :
		pass
	
	async def update(self, record) :
		pass
	
	async def drop(self, record) :
		pass
	
	async def dropByID(self, modelClass, id) :
		pass
	
	async def createTable(self) :
		pass
	
	async def getExistingTable(self) :
		pass