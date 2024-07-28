from xerial.DBSessionBase import DBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector
from xerial.ForeignKey import ForeignKey
from xerial.StringColumn import StringColumn
from xerial.ExcelWriter import ExcelWriter
from xerial.Record import Record
from xerial.Modification import Modification
from typing import Dict, List, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import TypeVar

import logging, csv, xlsxwriter, time, os, json



T = TypeVar("T")

class AsyncDBSessionBase (DBSessionBase) :
	async def checkModification(self, versionPath:str) :
		if os.path.isfile(versionPath) :
			with open(versionPath) as fd :
				modelVersion = json.load(fd)
			for name, model in self.model.items():
				current = modelVersion.get(name, None)
				if current is not None :
					last = await self.checkModelModification(model, current)
				else :
					last = self.getLastVersion(model)
				modelVersion[name] = str(last)
		else :
			modelVersion = {}
			for name, model in self.model.items():
				last = self.getLastVersion(model)
				modelVersion[name] = str(last)

		with open(versionPath, 'wt') as fd:
			raw = json.dump(modelVersion, fd, indent=4)

	async def init(self, modificationPath: str=None):# -> Self:
		modelList = DBSessionBase.REGISTERED_MODEL[:]
		DBSessionBase.REGISTERED_MODEL = []
		for modelClass in modelList:
			self.appendModel(modelClass)
		if modificationPath is None:
			modificationPath = os.path.abspath('./ModelVersion.json')
		await self.connect()
		await self.checkModification(modificationPath)
		await self.createTable()
		self.checkModelLinking()
		return self

	async def injectModel(self):
		for name, model in self.model.items():
			injected = Record.getInjectedColumn(name)
			existingColumn = set([i.lower() for i in await self.getDBColumnName(model)])
			for columnName, column  in injected.items():
				column.vendor = self.vendor
				model.meta.append((columnName, column))
				if columnName.lower() not in existingColumn:
					query = Modification.generateAddQuery(self.vendor, model, column)
					await self.executeWrite(query)
			self.prepareStatement(model)

	async def checkModelModification(self, modelClass, currentVersion) :
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
		self.lastConnectionTime = time.time()
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
	
	async def selectRaw(self, modelClass:type, clause:str, limit:int=None, offset:int=None, parameter:list=None) -> dict :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = await self.executeRead(query, parameter)
		result = []
		for row in cursor :
			data = {}
			i = 0
			for columnName, column in modelClass.meta :
				data[columnName] = column.toDict(row[i])
				i += 1
			result.append(data)
		return result

	def convertRaw(self, fetched) :
		for i in fetched :
			for k, v in i.items() :
				if isinstance(v, datetime) :
					i[k] = v.strftime("%Y-%m-%d %H:%M:%S")
				elif isinstance(v, date) :
					i[k] = v.strftime("%Y-%m-%d")
				elif isinstance(v, Decimal) :
					i[k] = float(v)
				elif isinstance(v, timedelta) :
					i[k] = v.seconds
				elif isinstance(v, bytes) :
					i[k] = v.hex()
		return fetched
	
	# NOTE : Return None if not found.
	async def selectByID(self, modelClass:T, ID:int, isRelated:bool=False, hasChildren:bool=False) -> T :
		fetched = await self.select(
			modelClass,
			f"WHERE {modelClass.primary}=?",
			parameter = [int(ID)],
			limit=1,
			isRelated=isRelated,
			hasChildren=hasChildren
		)
		if len(fetched) : return fetched[0]
		else : None

	async def select(self, modelClass:T, clause:str, isRelated:bool=False, hasChildren:bool=False, limit:int=None, offset:int=None, parameter:list=None) -> List[T]:
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = await self.executeRead(query, parameter)
		result = []
		for row in cursor :
			record = modelClass.__new__(modelClass)
			record.initRelation()
			i = 0
			for columnName, column in modelClass.meta :
				setattr(record, columnName, column.processValue(row[i]))
				i += 1
			result.append(record)
		if isRelated and len(result) :
			await self.selectRelated(modelClass, result)
		if hasChildren and len(result) :
			await self.selectChildren(modelClass, result)
		return result
	
	async def selectTranspose(self, modelClass:type, clause:str, isRelated:bool=False, hasChildren:bool=False, limit:int=None, offset:int=None, parameter:list=None) -> dict :
		recordList = await self.select(modelClass, clause, isRelated, hasChildren, limit, offset, parameter)
		result = {}
		for name, column in modelClass.meta :
			result[name] = []
		for record in recordList :
			data = record.toDict()
			for name, column in modelClass.meta :
				result[name].append(data[name])
		return result

	# NOTE
	# For writing string descriptor = io.StringIO()
	async def selectCSV(self, descriptor, modelClass:type, clause:str, limit:int, offset:int, parameter:list=None) :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = await self.executeRead(query, parameter)
		writer = csv.writer(descriptor)
		columnNameList = [columnName for columnName, _ in modelClass.meta]
		writer.writerow(columnNameList)
		for row in cursor :
			writer.writerow(row)
	
	async def selectExcel(self, fileName:str, modelClass:type, clause:str, limit:int=None, offset:int=None, parameter:list=None) :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = await self.executeRead(query, parameter)
		self.checkLinkingMeta(modelClass)
		with xlsxwriter.Workbook(fileName) as workbook :
			writer = ExcelWriter(modelClass, workbook)
			writer.writeMain(cursor)
			for foreignKey in modelClass.foreignKey :
				clause = writer.getForeignClause(foreignKey)
				query = self.generateSelectQuery(foreignKey.model, clause, None, None)
				cursor = await self.executeRead(query, None)
				writer.writeForeign(foreignKey, cursor)
			writer.writeReference()

	async def selectRelated(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		self.checkLinkingMeta(modelClass)
		isMapper = modelClass.__is_mapper__
		for foreignKey in modelClass.foreignKey :
			keyList = [getattr(i, foreignKey.name) for i in recordList]
			keyList = [i for i in keyList if i is not None]
			if len(keyList) :
				if isinstance(foreignKey.columnMeta, StringColumn) :
					keyList = {f"'{i}'" for i in keyList}
				else :
					keyList = {str(i) for i in keyList}
				
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
		if isinstance(primary, StringColumn) :
			keyList = [f"'{getattr(i, primary.name)}'" for i in recordList]
		else :
			keyList = [str(getattr(i, primary)) for i in recordList]
		joined = ','.join(list(keyList))
		childrenMap = {}
		childrenFlattedMap = {}
		for child in modelClass.children :
			clause = f"WHERE {child.parentColumn} IN ({joined})"
			childRecord = await self.select(child.model, clause, False)
			childrenFlattedMap[child.name] = childRecord
			columnMap = {}
			childrenMap[child.name] = columnMap
			for record in childRecord :
				parent = getattr(record, child.parentColumn)
				childrenList = columnMap.get(parent, [])
				if len(childrenList) == 0 : columnMap[parent] = childrenList
				childrenList.append(record)
		
		for child in modelClass.children :
			if not child.model.__is_mapper__ : continue
			childRecordList = childrenFlattedMap[child.name]
			for foreignKey in child.model.foreignKey :
				foreignKey: ForeignKey
				if foreignKey.model is None:
					foreignKey.model = self.model.get(foreignKey.modelName, None)
				if foreignKey.model == modelClass : continue
				if isinstance(foreignKey.columnMeta, StringColumn) :
					keyList = {f"'{getattr(i, foreignKey.name)}'" for i in childRecordList}
				else :
					keyList = {str(getattr(i, foreignKey.name)) for i in childRecordList}
				if len(keyList) == 0: continue
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

	async def insertChildren(self, record, modelClass, isReturningID=True) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if len(childRecordList) == 0 : continue
			if not isinstance(childRecordList, list) : continue
			for childRecord in childRecordList :
				setattr(childRecord, child.parentColumn, primary)
			await self.insertMultiple(childRecordList, isReturningID=isReturningID)
	
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
					setattr(childRecord, child.parentColumn, primary)
			await self.insertMultiple(insertList, isReturningID=True)
	
	async def dropChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__full_table_name__
			query = f"DELETE FROM {table} WHERE {child.column}={primary}"
			await self.executeWrite(query)

	async def dropChildrenByID(self, recordID, modelClass) :
		self.checkLinkingMeta(modelClass)
		for child in modelClass.children :
			table = child.model.__full_table_name__
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
	
	async def insertMultipleDirect(self, modelClass, rawList) :
		pass

	async def update(self, record) :
		pass
	
	async def updateDirect(self, modelClass, raw) :
		pass
	
	async def drop(self, record) :
		pass
	
	async def dropByID(self, modelClass, id) :
		pass
	
	async def dropByCondition(self, modelClass, condition) :
		pass
	
	async def setFieldByID(self, modelClass:type, fieldMap:Dict[str, Any], id:int) :
		query, parameter = self.generateSetField(modelClass, fieldMap, id)
		query = self.processClause(query, parameter)
		await self.executeWrite(query, parameter)

	async def setFieldByIDList(self, modelClass:type, fieldMap:Dict[str, Any], ids:List[int]) :
		query, parameter = self.generateSetFieldIDList(modelClass, fieldMap, ids)
		if query is None : return
		query = self.processClause(query, parameter)
		await self.executeWrite(query, parameter)
	
	async def resetIDSequence(self, modelClass:type, renewStartID:int) :
		query = self.generateResetID(modelClass)
		if query is None : return
		parameter = [int(renewStartID)]
		query = self.processClause(query, parameter)
		await self.executeWrite(query, parameter)

	async def createTable(self) :
		pass
	
	async def getExistingTable(self) :
		pass

	async def getDBColumnName(self, model: type) -> List[str]:
		raise NotADirectoryError