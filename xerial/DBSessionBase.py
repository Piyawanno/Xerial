import json
from xerial.Column import Column
from xerial.CurrencyColumn import CurrencyColumn
from xerial.CurrencyData import CurrencyData
from xerial.Record import Record
from xerial.IntegerColumn import IntegerColumn
from xerial.StringColumn import StringColumn
from xerial.RoundRobinConnector import RoundRobinConnector
from xerial.ExcelWriter import ExcelWriter
from enum import Enum
from packaging.version import Version
from typing import Dict, List, Any, Tuple

import logging, csv, xlsxwriter, os, json

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
		self.lastConnectionTime = -1.0
		self.parentMap = {}
	
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
		"""
		Insert record into database.

		Parameters
		----------
		record: Object of class Record or its inheritance to insert into database.
		
		isAutoID: If setting to True, primary key of the record will be
		auto generated from database. Otherwise, the primary key must be set.
		"""
		pass
	
	def insertMultiple(self, recordList, isAutoID=True, isReturningID=False) :
		"""
		Insert list of records into database.

		Parameters
		----------
		recordList: List of Object of class Record or its inheritance to insert into database.
		
		isAutoID: If setting to True, primary key of the record will be
		auto generated from database. Otherwise, the primary key must be set.
		
		isReturningID: If setting to False and isAutoID=True,
		Although the primary key of the record will be auto generated,
		it will not set to the record due to the performance reason.
		"""
		pass

	def insertMultipleDirect(self, modelClass, rawList) :
		pass
	
	def update(self, record) :
		pass
	
	def updateDirect(self, modelClass, raw) :
		pass
	
	def drop(self, record) :
		pass
	
	def dropByID(self, modelClass, id) :
		pass

	def dropByCondition(self, modelClass, condition) :
		pass

	def setFieldByID(self, modelClass:type, fieldMap:Dict[str, Any], id:int) :
		query, parameter = self.generateSetField(modelClass, fieldMap, id)
		if query is None : return
		query = self.processClause(query, parameter)
		self.executeWrite(query, parameter)

	def setFieldByIDList(self, modelClass:type, fieldMap:Dict[str, Any], ids:List[int]) :
		query, parameter = self.generateSetFieldIDList(modelClass, fieldMap, ids)
		if query is None : return
		query = self.processClause(query, parameter)
		self.executeWrite(query, parameter)

	def createTable(self) :
		pass
	
	def getExistingTable(self) -> List[str] :
		pass

	def resetIDSequence(self, modelClass:type, renewStartID:int) :
		query = self.generateResetID(modelClass)
		parameter = [int(renewStartID)]
		query = self.processClause(query, parameter)
		self.executeWrite(query, parameter)
	
	def dropTable(self, modelClass:type) :
		existing = {i.lower() for i in self.getExistingTable()}
		if modelClass.__fulltablename__.lower() in existing :
			query = self.generateDropTable(modelClass)
			self.executeWrite(query)

	def generateResetID(self, modelClass:type) -> str :
		return ""
	
	def generateDropTable(self, modelClass:type) -> str :
		return f"DROP TABLE {modelClass.__fulltablename__}"
	
	def appendModel(self, modelClass) :
		self.model[modelClass.__name__] = modelClass
		if Record.hasMeta(modelClass) : return
		Record.checkTableName(modelClass, self.prefix)
		Record.extractMeta(modelClass)
		# Record.extractInput(modelClass)
		Record.setVendor(modelClass, self.vendor)
		self.prepareStatement(modelClass)
		self.getParent(modelClass)

	def getParent(self, modelClass) :
		record = modelClass.__new__(modelClass)
		parentModel:str = record.setAsChildrenOf()
		if parentModel is not None :
			splitted = parentModel.split('.')
			parentModelName = splitted[0]
			columnName = splitted[1]
			childrenList = self.parentMap.get(parentModelName, [])
			if len(childrenList) == 0 : self.parentMap[parentModelName] = childrenList
			childrenList.append((columnName, f'{modelClass.__name__}.{modelClass.primary}'))
	
	def checkModelLinking(self) :
		from xerial.Children import Children
		for modelClass in self.model.values() :
			additionalChildren = self.parentMap.get(modelClass.__name__, None)
			if additionalChildren is None : continue
			for attribute, child in additionalChildren :
				setattr(modelClass, attribute, Children(child))
			Record.extractChildren(modelClass)

		for modelClass in self.model.values() :
			self.checkLinkingMeta(modelClass)
	
	def checkModification(self, versionPath:str) :
		"""
		Automatic checking of Structure Modification.

		Parameters
		----------
		versionPath : Path to JSON file storing the current version
		of each model.
		"""
		if os.path.isfile(versionPath) :
			with open(versionPath) as fd :
				modelVersion = json.load(fd)
		else :
			modelVersion = {}

		for name, model in self.model.items():
			current = modelVersion.get(name, '1.0')
			last = self.checkModelModification(model, current)
			modelVersion[name] = str(last)

		with open(versionPath, 'wt') as fd:
			raw = json.dumps(modelVersion, indent=4)
			fd.write(raw)
	
	def checkModelModification(self, modelClass, currentVersion) :
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
	
	def generateSelectQuery(self, modelClass:type, clause:str, limit:int, offset:int) -> str :
		return ''
	
	def generateRawSelectQuery(self, tableName, clause, limit=None, offset=None) :
		return ''
	
	def count(self, modelClass:type, clause:str, parameter:list=None) -> int :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateCountQuery(modelClass, clause)
		cursor = self.executeRead(query, parameter)
		for i in cursor :
			return i[0]
	
	# NOTE : Return None if not found.
	def selectByID(self, modelClass:type, ID:int, isRelated:bool=False, isChildren:bool=False) -> Record :
		fetched = self.select(
			modelClass,
			f"WHERE {modelClass.primary}=?",
			parameter = [int(ID)],
			limit=1,
			isRelated=isRelated,
			isChildren=isChildren
		)
		if len(fetched) : return fetched[0]
		else : None

	def select(self,
			modelClass:type,
			clause:str,
			isRelated:bool=False,
			isChildren:bool=False,
			limit:int=None,
			offset:int=None,
			parameter:list=None
		) -> list:
		"""
		Select data from database.

		Parameters
		----------
		modelClass: Class of model to select
		
		clause: String of query clause, Xerial allows WHERE, ORDER BY, GROUP BY
		
		isRelated: By setting to True, the related data with foreignKey
		will be selected. Otherwise, the foreignKey column will have
		the reference value.
		
		isChildren: By setting to True, the children records will be selected.
		
		limit: Maximum number of records to select. If setting to None=no limit.
		
		offset: Offset of records to select. If setting to None=no offset.
		
		parameter: List of query parameter for the '?' placement
		in the clause parameter.
		"""
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		import time
		cursor = self.executeRead(query, parameter)
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
			self.selectRelated(modelClass, result)
		if isChildren and len(result) :
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
	
	def selectRaw(self, modelClass:type, clause:str, limit:int=None, offset:int=None, parameter:list=None) -> dict :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = self.executeRead(query, parameter)
		result = []
		for row in cursor :
			data = {}
			i = 0
			for columnName, column in modelClass.meta :
				data[columnName] = column.toDict(row[i])
				i += 1
			result.append(data)
		return result

	# NOTE
	# For writing string descriptor = io.StringIO()
	def selectCSV(self, descriptor, modelClass:type, clause:str, limit:int=None, offset:int=None, parameter:list=None) :
		if parameter is not None :
			clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = self.executeRead(query, parameter)
		writer = csv.writer(descriptor)
		columnNameList = [columnName for columnName, _ in modelClass.meta]
		writer.writerow(columnNameList)
		for row in cursor :
			writer.writerow(row)
	
	def selectExcel(self, fileName:str, modelClass:type, clause:str, limit:int=None, offset:int=None, parameter:list=None) :
		if parameter is not None : clause = self.processClause(clause, parameter)
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = self.executeRead(query, parameter)
		self.checkLinkingMeta(modelClass)
		with xlsxwriter.Workbook(fileName) as workbook :
			writer = ExcelWriter(modelClass, workbook)
			writer.writeMain(cursor)
			for foreignKey in modelClass.foreignKey :
				clause = writer.getForeignClause(foreignKey)
				query = self.generateSelectQuery(foreignKey.model, clause, None, None)
				cursor = self.executeRead(query, None)
				writer.writeForeign(foreignKey, cursor)
			writer.writeReference()
	
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
			elif column.isConvertRaw :
				value.append(column.convertRaw(attribute))
			else :
				value.append(attribute)
		return value
	
	def toTuple(self, modelClass, raw) :
		result = []
		defaultCurrencyValue = CurrencyData(0).toDict()
		for name, column in modelClass.meta:
			if isinstance(column, CurrencyColumn): 
				result.append(json.dumps(raw.get(name, defaultCurrencyValue)))
			else: 
				result.append(column.fromDict(raw))
		return result
	
	def selectRelated(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		self.checkLinkingMeta(modelClass)
		isMapper = modelClass.__is_mapper__
		for foreignKey in modelClass.foreignKey :
			if isinstance(foreignKey.columnMeta, StringColumn) :
				keyList = {f"'{getattr(i, foreignKey.name)}'" for i in recordList}
			else :
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
		if isinstance(primary, StringColumn) :
			keyList = {f"'{getattr(i, primary.name)}'" for i in recordList}
		else :
			keyList = {str(getattr(i, primary)) for i in recordList}
		joined = ','.join(list(keyList))
		childrenMap = {}
		childrenFlattedMap = {}
		for child in modelClass.children :
			clause = f"WHERE {child.parentColumn} IN ({joined})"
			childRecord = self.select(child.model, clause, False)
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
				if foreignKey.model == modelClass : continue
				if isinstance(foreignKey.columnMeta, StringColumn) :
					keyList = {f"'{getattr(i, foreignKey.name)}'" for i in childRecordList}
				else :
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
				setattr(childRecord, child.parentColumn, primary)
			self.insertMultiple(childRecordList, isReturningID=True)
	
	def updateChildren(self, record, modelClass) :
		self.checkLinkingMeta(modelClass)
		primary = getattr(record, modelClass.primary)
		for child in modelClass.children :
			childRecordList = getattr(record, child.name)
			if not isinstance(childRecordList, list) : continue
			if len(childRecordList) == 0 : continue
			insertList = []
			for childRecord in childRecordList :
				childID = getattr(childRecord, child.model.primary, None)
				if childID is not None :
					self.update(childRecord)
				else :
					insertList.append(childRecord)
					setattr(childRecord, child.parentColumn, primary)
			self.insertMultiple(insertList, isReturningID=True)
	
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
		modelName = modelClass.__name__
		for child in modelClass.children :
			if child.model is None :
				childModelClass = self.model.get(child.modelName, None)
				if childModelClass is None :
					logging.warning(f"Child model {child.reference} for {modelClass.__name__} cannot be found.")
				child.model = childModelClass
				for foreignKey in childModelClass.foreignKey :
					if foreignKey.modelName == modelName :
						child.parentColumn = foreignKey.name
						break
		modelClass.isChildrenChecked = True
	
	def checkForeignKey(self, modelClass) :
		for foreignKey in modelClass.foreignKey :
			if foreignKey.model is None :
				model = self.model.get(foreignKey.modelName, None)
				if model is None :
					logging.warning(f"ForeignKey model {foreignKey.reference} for {modelClass.__name__} cannot be found.")
				else :
					foreignKey.model = model
					foreignKey.columnMeta = model.metaMap.get(foreignKey.column, None)
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
	
	def getRawPrimaryClause(self, modelClass, raw) :
		if not hasattr(modelClass, 'primaryMeta') :
			logging.warning(f"*** Warning {modelClass.__fulltablename__} has not primary key and cannot be referenced.")
			return
		meta = modelClass.primaryMeta
		if isinstance(meta, list) :
			clause = []
			for i in meta :
				ID = raw.get(i.name, None)
				if ID is not None :
					clause.append("%s=%s"%(i.name, meta.setValueToDB())	)
			return " AND ".join(clause)
		else :
			ID = raw.get(modelClass.primary, None)
			ID = meta.setValueToDB(ID)
			return "%s=%s"%(modelClass.primary, ID)

	def generateDropCommand(self) :
		for model in self.model.values() :
			print("DROP TABLE IF EXISTS %s;"%(model.__fulltablename__))
	
	def processClause(self, clause:str, parameter:list) -> str:
		return clause
	
	def generateSetField(self, modelClass:type, fieldMap:Dict[str, Any], id:int) -> Tuple[str, list]:
		setList = []
		parameter = []
		for name, value in fieldMap.items():
			setList.append(f'{name}=?')
			parameter.append(value)
		parameter.append(id)
		query = "UPDATE %s SET %s WHERE %s=?"%(
			modelClass.__fulltablename__,
			",".join(setList),
			modelClass.primary
		)
		return query, parameter
	
	def generateSetFieldIDList(self, modelClass:type, fieldMap:Dict[str, Any], ids:List[int]) -> Tuple[str, list]:
		setList = []
		parameter = []
		for name, value in fieldMap.items():
			if name not in modelClass.metaMap : continue
			setList.append(f'{name}=?')
			parameter.append(value)
		if len(setList) == 0 : return None, None
		parameter.extend(ids)
		query = "UPDATE %s SET %s WHERE %s IN (%s)"%(
			modelClass.__fulltablename__,
			",".join(setList),
			modelClass.primary,
			",".join('?'*len(ids))
		)
		return query, parameter