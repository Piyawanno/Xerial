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
	
	async def count(self, modelClass, clause) :
		query = self.generateCountQuery(modelClass, clause)
		cursor = await self.executeRead(query)
		for i in cursor :
			return i[0]

	async def select(self, modelClass, clause, isRelated=False, limit=None, offset=None, isDebug=False) :
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = await self.executeRead(query)
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
	
	async def selectTranspose(self, modelClass, clause, isRelated=False, limit=None, offset=None, isDebug=False) :
		recordList = await self.select(modelClass, clause, isRelated, limit, offset)
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
		for attribute, table, primary in modelClass.foreignKey :
			keyList = [str(getattr(i, attribute)) for i in recordList]
			clause = "WHERE %s IN(%s)"%(primary, ",".join(keyList))
			related = await self.select(self.model[table], clause, False)
			relatedMap = {getattr(i, primary):i for i in related}
			for record in recordList :
				value = getattr(record, attribute)
				setattr(record, attribute, relatedMap.get(value, value))
	
	async def selectChildren(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
		primary = modelClass.primary
		keyList = [str(getattr(i, primary)) for i in recordList]
		joined = ','.join(keyList)
		childrenMap = {}
		for child in modelClass.children :
			clause = f"WHERE {child.column} IN ({joined})"
			childRecord = await self.select(child.model, clause, False)
			columnMap = {}
			childrenMap[child.name] = columnMap
			for record in childRecord :
				parent = getattr(record, child.column)
				childrenList = columnMap.get(parent, [])
				if len(childrenList) == 0 : columnMap[parent] = childrenList
				childrenList.append(record)
		
		for child in modelClass.children :
			for record in recordList :
				primary = getattr(record, modelClass.primary)
				setattr(record, child.name, childrenMap[child.name].get(primary, []))

	async def insertChildren(self, record, modelClass) :
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if len(childRecordList) == 0 : continue
			for childRecord in childRecordList :
				setattr(childRecord, child.column, primary)
			await self.insertMultiple(childRecordList)
	
	async def updateChildren(self, record, modelClass) :
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if len(childRecordList) == 0 : continue
			for childRecord in childRecordList :
				await self.update(childRecord)
	
	async def dropChildren(self, record, modelClass) :
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {table} WHERE {child.column}={primary}"
			await self.executeWrite(query)

	async def dropChildrenByID(self, recordID, modelClass) :
		if not modelClass.isChildrenChecked : self.checkChildren(modelClass)
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
	
	async def insert(self, record) :
		pass
	
	async def insertMultiple(self, recordList) :
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