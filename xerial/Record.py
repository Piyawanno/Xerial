from enum import IntEnum
from xerial.Column import Column
from xerial.Children import Children
from xerial.Input import Input
from xerial.Modification import Modification
from xerial.Vendor import Vendor

from packaging.version import Version
from typing import Dict, List, Type, Tuple

import inspect, logging, copy

__MAPPED_META__ = {}
__RESERVED__ = {
	'meta',
	'primaryMeta',
	'primitive',
	'representativeMeta',
	'__fulltablename__',
	'__tablename__',
}
__DEFAULT_BACKUP__ = False

def __getParentTableName__(modelClass) :
	hierarchy = list(inspect.getmro(modelClass))
	for parent in hierarchy[1:] :
		if hasattr(parent, '__tablename__') :
			return parent.__tablename__
	return None

def __getParentFullTableName__(modelClass) :
	hierarchy = list(inspect.getmro(modelClass))
	for parent in hierarchy[1:] :
		if hasattr(parent, '__fulltablename__') :
			return parent.__fulltablename__
	return None

class Record :
	def __init__(self, **kw) :
		modelClass = self.__class__
		if not hasattr(modelClass, 'meta') :
			Record.extractMeta(modelClass)
		self.initRelation(**kw)

	def initRelation(self, **kw) :
		modelClass = self.__class__
		for child in modelClass.children :
			setattr(self, child.name, [])
		for column, meta in modelClass.meta :
			setattr(self, column, kw.get(column, meta.default() if callable(meta.default) else meta.default))

	
	def toOption(self):
		return {
			'value': getattr(self, self.primaryMeta.name),
			'label': getattr(self, self.representativeMeta.name)
		}
	
	def toDict(self) -> dict :
		result = {}
		modelClass = self.__class__
		for child in modelClass.children :
			children = getattr(self, child.name)
			if isinstance(children, list) :
				result[child.name] = [i.toDict() for i in children]
		
		for foreignKey in modelClass.foreignKey :
			linked = getattr(self, foreignKey.name)
			if isinstance(linked, Record) and linked != self:
				if not hasattr(linked, '__raw__') :
					linked.__raw__ = linked.toDict()
				result[foreignKey.name] = linked.__raw__

		for column, meta in self.meta :
			if column == '__insert_time__' : continue
			if column == '__update_time__' : continue
			attribute = getattr(self, column)
			if attribute is None :
				result[column] = None
			elif meta != self :
				result[column] = meta.toDict(attribute() if callable(attribute) else attribute)
		return result
	
	def toRawDict(self) -> dict :
		result = {}
		for column, meta in self.meta :
			attribute = getattr(self, column)
			if attribute is None :
				result[column] = None
			elif meta != self :
				result[column] = meta.toDict(attribute)
		return result

	def fromDict(self, data:dict, isID:bool=False) :
		modelClass = self.__class__
		for child in modelClass.children :
			raw = data.get(child.name, None)
			if raw is not None :
				if isinstance(raw, list) :
					setattr(self, child.name, child.fromDict(raw))
				elif isinstance(raw, dict) :
					setattr(self, child.name, child.fromDict(raw.values()))
			
		for foreignKey in modelClass.foreignKey :
			raw = data.get(foreignKey.name, None)
			if raw is not None :
				if isinstance(raw, dict) :
					setattr(self, foreignKey.name, foreignKey.fromDict(raw))
				else :
					setattr(self, foreignKey.name, foreignKey.parent.parseValue(raw))

		meta:Column
		for column, meta in modelClass.meta :
			if column not in data : continue
			raw = data[column]
			if meta.foreignKey is None and isinstance(raw, dict) :
				setattr(self, column, meta.fromDict(raw))
			elif meta.foreignKey is None :
				setattr(self, column, meta.fromDict(data))
		if isID :
			self.id = data.get(modelClass.primary, 0)
		return self
	
	def fromRawDict(self, data:dict) :
		modelClass = self.__class__
		for column, meta in modelClass.meta :
			raw = data.get(column, None)
			if data is None :
				setattr(self, column, None)
			else :
				setattr(self, column, meta.fromDict(data))

	def dereference(self) :
		modelClass = self.__class__
		for foreignKey in modelClass.foreignKey :
			linked = getattr(self, foreignKey.name)
			if linked is None : continue
			if isinstance(linked, Record) :
				setattr(self, foreignKey.name, getattr(linked, foreignKey.model.primary))
	
	def copy(self, other) :
		for column, meta in self.meta :
			if hasattr(other, column) :
				setattr(self, column, getattr(other, column))
	
	def createModification(self, version:str) :
		"""
		Create a Modification object to modify Structure of Model.

		Parameters
		----------
		version: String of the new version of modification e.g. '2.0'.
		"""
		modelClass = self.__class__
		if not hasattr(modelClass, '__modification__') :
			modelClass.__modification__ = []
		modification = Modification(
			version,
			modelClass.__fulltablename__,
			modelClass.meta,
			modelClass.vendor
		)
		modelClass.__modification__.append(modification)
		return modification
	
	def modify(self) :
		"""
		A placeholder method for Structure Modification. By calling
		DBSession.checkModification(), this method of each Model
		registered to the DBSession will be called. To implement
		Structure Modification, this method must be overridden
		by creating Modification object with the method
		Record.createModification()
		"""
		pass

	def setAsChildrenOf(self) :
		return None
	
	@staticmethod
	def hasMeta(modelClass) :
		hasMeta = hasattr(modelClass, 'meta')
		mapped = modelClass in __MAPPED_META__
		if hasMeta and not mapped : hasMeta = False
		return hasMeta
	
	@staticmethod
	def hasParent(modelClass) :
		hasMeta = hasattr(modelClass, 'meta')
		if not hasMeta : return False
		mapped = modelClass in __MAPPED_META__
		return not mapped

	@staticmethod
	def setVendor(modelClass, vendor) :
		modelClass.vendor = vendor
		for column, meta in modelClass.meta :
			meta.vendor = vendor
		
		if modelClass.vendor == Vendor.POSTGRESQL :
			modelClass.__tablename__ = modelClass.__tablename__.lower()
			modelClass.__fulltablename__ = modelClass.__fulltablename__.lower()

	@staticmethod
	def extractInput(modelClass, extendedInput:List[Input]=[]) :
		inputPerLine = getattr(modelClass, 'inputPerLine', 2)
		order = 1
		inputList:List[Dict] = []
		mergedInput:List[Input] = []
		groupedInputList = []
		inputGroupMapper:Dict[int, List[Input]] = {}
		hasDefaultCallable = False
		modelClass.fileInput = []
		for i, attribute in modelClass.meta :
			if not isinstance(attribute, Column) : continue
			if attribute.input is None : continue
			attribute.input.columnType = attribute.__class__.__name__
			attribute.input.columnName = i
			mergedInput.append(attribute.input)
			if getattr(attribute, 'isFile', False) :
				modelClass.fileInput.append(attribute)
		mergedInput.extend(extendedInput)

		for i in mergedInput :
			input:Dict = i.toDict()
			if not 'order' in input or input['order'] is None:
				input['order'] = f'{order}.0'
			input['parsedOrder'] = Version(input['order'])
			input['isGroup'] = False
			input['inputPerLine'] = inputPerLine
			default = getattr(attribute, 'default', None)
			if not hasDefaultCallable : hasDefaultCallable = callable(default)
			input['default'] = default
			inputList.append(input)
			order += 1
			if i.group is None: 
				groupedInputList.append(copy.copy(input))
				continue
			if not i.group in inputGroupMapper:
				inputGroupMapper[i.group] = []
			inputGroupMapper[i.group].append(input)
		modelClass.__has_callable_default__ = hasDefaultCallable
		inputList.sort(key=lambda x : x['parsedOrder'])
		Record.extractGroupInput(modelClass, inputGroupMapper, groupedInputList)
		groupedInputList.sort(key=lambda x : x['parsedOrder'])
		modelClass.input = []
		for item in groupedInputList:
			del item['parsedOrder']
			modelClass.input.append(item)
		for item in inputList:
			if 'parsedOrder' in item: del item['parsedOrder']
		modelClass.inputDict = inputList

	@staticmethod
	def extractGroupInput(modelClass, inputGroupMapper, groupedInputList:list=[]) :
		inputPerLine = getattr(modelClass, 'inputPerLine', 2)
		group:IntEnum = getattr(modelClass, '__group_label__', None)
		addition = getattr(modelClass, '__addition_group__', None)
		if group is None and addition is None : return
		groupParsedOrder = []
		def groupInput(parsedOrder) :
			if parsedOrder['id'] in inputGroupMapper:
				inputGroupMapper[parsedOrder['id']].sort(key=lambda x : x['parsedOrder'])
				parsedOrder['input'] = []
				for item in inputGroupMapper[parsedOrder['id']]:
					del item['parsedOrder']
					parsedOrder['input'].append(item)
			groupedInputList.append(parsedOrder)
			groupParsedOrder.append(parsedOrder)

		for i in group.order:
			parsedOrder = {
				'id': i.value,
				'label': i.label[i],
				'order': group.order[i],
				'isGroup': True,
				'inputPerLine': inputPerLine
			}
			parsedOrder['parsedOrder'] = Version(group.order[i])
			groupInput(parsedOrder)
		
		if addition is not None :
			for i in addition.values() :
				i['parsedOrder'] = Version(i['order'])
				groupInput(i)

		groupParsedOrder.sort(key=lambda x : x['parsedOrder'])
		groupParsedOrder = [{'id': i['id'], 'label': i['label'], 'order': i['order']} for i in groupParsedOrder]
		modelClass.inputGroup = groupParsedOrder

	@staticmethod
	def extractMeta(modelClass) :
		if not hasattr(modelClass, '__version__') :
			modelClass.__version__ = '1.0'
		if not hasattr(modelClass, '__is_mapper__') :
			modelClass.__is_mapper__ = False
		if not hasattr(modelClass, '__skip_create__') :
			modelClass.__skip_create__ = False
		
		modelClass.representativeMeta = None
		modelClass.isForeignChecked = False
		modelClass.isChildrenChecked  = False
		if not Record.hasParent(modelClass) :
			primaryMeta = Record.checkPrimary(modelClass)
		else :
			if hasattr(modelClass, '__has_primary__') and modelClass.__has_primary__ :
				primaryMeta = modelClass.primaryMeta
				modelClass.meta = [(modelClass.primary, primaryMeta)]
			else :
				primaryMeta = None
		Record.checkBackup(modelClass)
		Record.extractAttribute(modelClass, primaryMeta)
		Record.extractChildren(modelClass)
		__MAPPED_META__[modelClass] = modelClass.meta

	@staticmethod
	def checkPrimary(modelClass) :
		from xerial.IntegerColumn import IntegerColumn
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if not isinstance(attribute, Column) : continue
			if not attribute.isPrimary : continue
			modelClass.__has_primary__ = True
		if not hasattr(modelClass, '__has_primary__') :
			modelClass.__has_primary__ = True
			modelClass.primary = 'id'
			primaryMeta = IntegerColumn(isPrimary=True)
			primaryMeta.name = 'id'
			modelClass.meta = [('id', primaryMeta)]
			return primaryMeta
		elif not modelClass.__has_primary__ :
			modelClass.meta = []
			return None
	
	@staticmethod
	def extractAttribute(modelClass, primaryMeta) :
		modelClass.foreignKey = []
		parentMetaMap = getattr(modelClass, 'metaMap', {})
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if i in __RESERVED__ : continue
			if i in parentMetaMap :
				modelClass.meta.append((i, parentMetaMap[i]))
				if isinstance(attribute, Column) and attribute.foreignKey is not None :
					attribute.foreignKey.name = i
					modelClass.foreignKey.append(attribute.foreignKey)
			elif isinstance(attribute, Column) :
				attribute.name = i
				if attribute.isRepresentative :
					if modelClass.representativeMeta is None :
						modelClass.representativeMeta = attribute
					else :
						logging.warning("Multiple representative columns are defined.")
				if attribute.foreignKey is not None :
					attribute.foreignKey.name = i
					modelClass.foreignKey.append(attribute.foreignKey)
				if attribute.isPrimary :
					if not hasattr(modelClass, 'primary') :
						modelClass.primary = i
						primaryMeta = attribute
					elif isinstance(modelClass.primary, list) :
						if i not in modelClass.primary :
							modelClass.primary.append(i)
							primaryMeta.append(attribute)
					elif  modelClass.primary != i :
						modelClass.primary = [i]
						primaryMeta = [primaryMeta]
				modelClass.meta.append((i, attribute))
				setattr(modelClass, i, attribute.default)
		modelClass.metaMap = {k:v for k, v in modelClass.meta}
		if primaryMeta is not None :
			modelClass.primaryMeta = primaryMeta
	
	@staticmethod
	def extractChildren(modelClass) :
		modelClass.children = []
		modelClass.isChildrenChecked = False
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if isinstance(attribute, Children) :
				attribute.name = i
				modelClass.children.append(attribute)

	@staticmethod
	def parseTime(delta):
		hours, remainder = divmod(delta.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		return "%02d:%02d:%02d"%(hours, minutes, seconds)
	
	@staticmethod
	def checkTableName(modelClass, prefix:str) :
		hasTableName = hasattr(modelClass, '__tablename__')
		parentTableName = __getParentTableName__(modelClass)
		if not hasTableName or parentTableName == modelClass.__tablename__ :
			modelClass.__tablename__ = f"{prefix}{modelClass.__name__}"
		tableName = modelClass.__tablename__
		if prefix is not None and len(prefix) :
			if tableName[:len(prefix)] != prefix :
				modelClass.__tablename__ = f"{prefix}{tableName}"
		hasFullName = hasattr(modelClass, '__fulltablename__')
		parentFullName = __getParentFullTableName__(modelClass)
		if not hasFullName or parentFullName == modelClass.__fulltablename__ :
			hasPrefix = False
			if prefix is not None and len(prefix) :
				if modelClass.__tablename__[:len(prefix)] != prefix :
					modelClass.__fulltablename__ = f"{prefix}{modelClass.__tablename__}"
					hasPrefix = True
			if not hasPrefix :
				modelClass.__fulltablename__ = modelClass.__tablename__
	
	@staticmethod
	def enableDefaultBackup() :
		global __DEFAULT_BACKUP__
		__DEFAULT_BACKUP__ = True

	@staticmethod
	def checkBackup(modelClass) :
		from xerial.FloatColumn import FloatColumn
		if not hasattr(modelClass, '__backup__') : modelClass.__backup__ = __DEFAULT_BACKUP__
		if not modelClass.__backup__ : return
		modelClass.__insert_time__ = FloatColumn(isIndex=True, default=-1.0)
		modelClass.__update_time__ = FloatColumn(isIndex=True, default=-1.0)
	
	@staticmethod
	def appendGroup(modelClass, label:str, value:int, order:str, inputPerLine:int=2) :
		if not hasattr(modelClass, '__addition_group__') :
			modelClass.__addition_group__ = {}
		modelClass.__addition_group__[value] = {
			'id': value,
			'label': label,
			'order': order,
			'isGroup': True,
			'inputPerLine' : inputPerLine,
		}
	
	@staticmethod
	def disableInput(modelClass, columnName:str) :
		column = getattr(modelClass, columnName, None)
		if column is None : return
		if not hasattr(column, 'input') : return
		column.input = None

	@staticmethod
	def replaceInput(modelClass, columnName:str, input:Input) :
		column = getattr(modelClass, columnName, None)
		if column is None : return
		if not hasattr(column, 'input') : return
		column.input = input