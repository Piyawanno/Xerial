from xerial.Column import Column
from xerial.Record import Record
from xerial.IntegerColumn import IntegerColumn
from xerial.RoundRobinConnector import RoundRobinConnector
from enum import Enum
from packaging import version

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
	
	def insert(self, record) :
		pass
	
	def insertMultiple(self, recordList) :
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
	
	def checkModification(self, modelClass, currentVersion) :
		modificationList = self.generateModification(modelClass, currentVersion)
		lastVersion = currentVersion
		for v, queryList in modificationList :
			lastVersion = v
			for query in queryList :
				self.executeWrite(query)
		return str(lastVersion)

	def generateModification(self, modelClass, currentVersion) :
		currentVersion = version.parse(currentVersion)
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
	
	def count(self, modelClass, clause) :
		query = self.generateCountQuery(modelClass, clause)
		cursor = self.executeRead(query)
		for i in cursor :
			return i[0]

	def select(self, modelClass, clause, isRelated=False, limit=None, offset=None, isDebug=False) :
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = self.executeRead(query)
		result = []
		for row in cursor :
			record = modelClass()
			i = 0
			for columnName, column in modelClass.meta :
				setattr(record, columnName, column.processValue(row[i]))
				i += 1
			result.append(record)
		if isRelated : self.selectRelated(modelClass, result)
		return result
	
	def selectTranspose(self, modelClass, clause, isRelated=False, limit=None, offset=None, isDebug=False) :
		recordList = self.select(modelClass, clause, isRelated, limit, offset)
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
			if isinstance(attribute, Enum) :
				value.append(attribute.value)
			else :
				value.append(attribute)
		return value
	
	def selectRelated(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		isMapper = hasattr(modelClass, '__is_mapper__') and modelClass.__is_mapper__
		for attribute, table, primary in modelClass.foreignKey :
			keyList = [str(getattr(i, attribute)) for i in recordList]
			clause = "WHERE %s IN(%s)"%(primary, ",".join(keyList))
			related = self.select(self.model[table], clause, isMapper)
			relatedMap = {getattr(i, primary):i for i in related}
			for record in recordList :
				value = getattr(record, attribute)
				setattr(record, attribute, relatedMap.get(value, value))
	
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