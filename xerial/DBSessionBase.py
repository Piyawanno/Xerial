from xerial.Column import Column
from xerial.Record import Record
from xerial.IntegerColumn import IntegerColumn
from xerial.RoundRobinConnector import RoundRobinConnector
from enum import Enum
from packaging.version import Version

import logging

class PrimaryDataError (Exception) :
	pass

class DBSessionBase :
	def __init__(self, config) :
		self.config = config
		self.prefix = config.get("prefix", "")
		self.vendor = config['vendor']
		self.isRoundRobin = config.get("isRoundRobin", False)
		self.model = {}
		self.mapExecute()
		self.queryCount = 0
	
	def resetCount(self) :
		self.queryCount = 0

	def mapExecute(self) :
		if self.isRoundRobin :
			self.executeRead = self.executeRoundRobinRead
			self.executeWrite = self.executeRoundRobinWrite
		else :
			self.executeRead = self.executeRegularRead
			self.executeWrite = self.executeRegularWrite
	
	def createConnection(self) :
		pass
	
	def closeConnection(self) :
		pass
	
	def executeRead(self, query, parameter=None) :
		pass
	
	def executeWrite(self, query, parameter=None) :
		pass
	
	def insert(self, record, isAutoID=True) :
		pass
	
	def insertMultiple(self, recordList, isAutoID=True, isReturningID=False) :
		pass
	
	def update(self, record) :
		pass
	
	def drop(self, record) :
		pass
	
	def dropByID(self, modelClass, id) :
		pass
	
	def createTable(self) :
		pass
	
	def getExistingTable(self) :
		pass
	
	def appendModel(self, modelClass) :
		self.model[modelClass.__name__] = modelClass
		if hasattr(modelClass, 'meta') : return
		self.checkTableName(modelClass)
		Record.extractInput(modelClass)
		Record.extractMeta(modelClass)
		Record.setVendor(modelClass, self.vendor)
		self.prepareStatement(modelClass)
	
	def checkModelLinking(self) :
		for modelClass in self.model.values() :
			self.checkLinkingMeta(modelClass)
	
	def checkModification(self, modelClass, currentVersion) :
		modificationList = self.generateModification(modelClass, currentVersion)
		lastVersion = currentVersion
		for v, queryList in modificationList :
			lastVersion = v
			for query in queryList :
				self.executeWrite(query)
		return str(lastVersion)

	def generateModification(self, modelClass, currentVersion) :
		currentVersion = Version(currentVersion)
		queryList = []
		record = modelClass.__new__(modelClass)
		record.modify()
		if not hasattr(modelClass, '__modification__') : return queryList
		for i in modelClass.__modification__ :
			if i.version > currentVersion :
				queryList.append((i.version, i.generateQuery()))
		return queryList
	
	def prepareStatement(self, modelClass) :
		pass

	def checkTableName(self, modelClass) :
		prefix = self.prefix
		if not hasattr(modelClass, '__tablename__') :
			modelClass.__tablename__ = f"{prefix}{modelClass.__name__}"
		tableName = modelClass.__tablename__
		if prefix is not None and len(prefix) :
			if tableName[:len(prefix)] != prefix :
				modelClass.__tablename__ = f"{prefix}{tableName}"
		if not hasattr(modelClass, '__fulltablename__') :
			hasPrefix = False
			if prefix is not None and len(prefix) :
				if modelClass.__tablename__[:len(prefix)] != prefix :
					modelClass.__fulltablename__ = f"{prefix}{modelClass.__tablename__}"
					hasPrefix = True
			if not hasPrefix :
				modelClass.__fulltablename__ = modelClass.__tablename__

	def connect(self, connection=None) :
		if connection is not None :
			self.isRoundRobin = isinstance(connection, RoundRobinConnector)
			self.connection = connection
			self.cursor = self.connection.cursor()
		else :
			if self.isRoundRobin :
				self.connection = RoundRobinConnector(self.config)
				self.connection.connect(True)
			else :
				self.createConnection()
	
	def count(self, modelClass:type, clause:str, parameter:list=None) -> int :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateCountQuery(modelClass, clause)
		cursor = self.executeRead(query, parameter)
		for i in cursor :
			return i[0]

	def select(self, modelClass:type, clause:str, isRelated:bool=False, limit:int=None, offset:int=None, parameter:list=None) -> list:
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = self.executeRead(query, parameter)
		result = []
		for row in cursor :
			record = modelClass()
			i = 0
			for columnName, column in modelClass.meta :
				setattr(record, columnName, column.processValue(row[i]))
				i += 1
			result.append(record)
		if isRelated :
			self.selectRelated(modelClass, result)
			self.selectChildren(modelClass, result)
		return result
	
	def selectTranspose(self, modelClass:type, clause:str, isRelated:bool=False, limit:int=None, offset:int=None, parameter:list=None) -> dict :
		recordList = self.select(modelClass, clause, isRelated, limit, offset, parameter)
		result = {}
		for name, column in modelClass.meta :
			result[name] = []
		for record in recordList :
			data = record.toDict()
			for name, column in modelClass.meta :
				result[name].append(data[name])
		return result
	
	def getValue(self, record, isAutoID=True) :
		value = []
		meta = record.__class__.insertMeta if isAutoID else record.__class__.meta
		for columnName, column in meta :
			attribute = getattr(record, columnName)
			if isinstance(attribute, Column) or attribute is None :
				value.append('NULL')
			elif isinstance(attribute, Record) :
				value.append(column.setValueToDB(column.getReference(attribute)))
			else :
				value.append(column.setValueToDB(attribute))
		return value
	
	def getRawValue(self, record, isAutoID=True) :
		value = []
		meta = record.__class__.insertMeta if isAutoID else record.__class__.meta
		for columnName, column in meta :
			attribute = getattr(record, columnName)
			if isinstance(attribute, Column) :
				value.append(None)
			elif isinstance(attribute, Record) :
				value.append(column.getReference(attribute))
			elif isinstance(attribute, Enum) :
				value.append(attribute.value)
			else :
				value.append(attribute)
		return value
	
	def selectRelated(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		self.checkLinkingMeta(modelClass)
		isMapper = modelClass.__is_mapper__
		for foreignKey in modelClass.foreignKey :
			keyList = {str(getattr(i, foreignKey.name)) for i in recordList}
			clause = "WHERE %s IN(%s)"%(foreignKey.column, ",".join(list(keyList)))
			related = self.select(foreignKey.model, clause, isMapper)
			relatedMap = {getattr(i, foreignKey.column):i for i in related}
			for record in recordList :
				value = getattr(record, foreignKey.name)
				setattr(record, foreignKey.name, relatedMap.get(value, value))
	
	def selectChildren(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		self.checkLinkingMeta(modelClass)
		primary = modelClass.primary
		keyList = {str(getattr(i, primary)) for i in recordList}
		joined = ','.join(list(keyList))
		childrenMap = {}
		childrenFlattedMap = {}
		for child in modelClass.children :
			clause = f"WHERE {child.column} IN ({joined})"
			childRecord = self.select(child.model, clause, False)
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
				linkedList = self.select(foreignKey.model, f"WHERE {foreignKey.column} IN ({joined})", False)
				linkedMap = {getattr(i, foreignKey.model.primary):i for i in linkedList}
				for childRecord in childRecordList :
					key = getattr(childRecord, foreignKey.name)
					setattr(childRecord, foreignKey.name, linkedMap.get(key, None))

		for child in modelClass.children :
			for record in recordList :
				primary = getattr(record, modelClass.primary)
				setattr(record, child.name, childrenMap[child.name].get(primary, []))
	
	def insertChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if not isinstance(childRecordList, list) : continue
			if len(childRecordList) == 0 : continue
			for childRecord in childRecordList :
				setattr(childRecord, child.column, primary)
			self.insertMultiple(childRecordList)
	
	def updateChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if len(childRecordList) == 0 : continue
			for childRecord in childRecordList :
				self.update(childRecord)
	
	def dropChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {table} WHERE {child.column}={primary}"
			self.executeWrite(query)

	def dropChildrenByID(self, recordID, modelClass) :
		self.checkLinkingMeta(modelClass)
		for child in modelClass.children :
			table = child.model.__fulltablename__
			query = f"DELETE FROM {table} WHERE {child.column}={recordID}"
			self.executeWrite(query)
		
	def checkLinkingMeta(self, modelClass) :
		if not modelClass.isChildrenChecked :
			self.checkChildren(modelClass)
		if not modelClass.isForeignChecked :
			self.checkForeignKey(modelClass)

	def checkChildren(self, modelClass) :
		for child in modelClass.children :
			if child.model is None :
				childModelClass = self.model.get(child.modelName, None)
				if childModelClass is None :
					logging.warning(f"Child model {child.reference} for {modelClass.__name__} cannot be found.")
				child.model = childModelClass
		modelClass.isChildrenChecked = True
	
	def checkForeignKey(self, modelClass) :
		for foreignKey in modelClass.foreignKey :
			if foreignKey.model is None :
				model = self.model.get(foreignKey.modelName, None)
				if model is None :
					logging.warning(f"ForeignKey model {foreignKey.reference} for {modelClass.__name__} cannot be found.")
				foreignKey.model = model
		modelClass.isForeignChecked = True
	
	def getPrimaryClause(self, record) :
		modelClass = record.__class__
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be referenced.")
			return
		meta = modelClass.primaryMeta
		if isinstance(meta, list) :
			clause = []
			for i in meta :
				ID = meta.setValueToDB(getattr(record, i.name))
				clause.append("%s=%s"%(i.name, ID)	)
			return " AND ".join(clause)
		else :
			ID = meta.setValueToDB(getattr(record, modelClass.primary))
			return "%s=%s"%(record.__class__.primary, ID)

	def generateDropCommand(self) :
		for model in self.model.values() :
			print("DROP TABLE IF EXISTS %s;"%(model.__fulltablename__))
	
	def processClause(self, clause:str, parameter:list) -> str:
		return clause