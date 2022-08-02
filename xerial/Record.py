from dataclasses import dataclass

from xerial.Column import Column
from xerial.Children import Children
from xerial.Input import Input
from xerial.Modification import Modification
from packaging.version import Version
from typing import List, Type

class Record :
	def __init__(self, **kw) :
		modelClass = self.__class__
		if not hasattr(modelClass, 'meta') :
			Record.extractMeta(modelClass)
		for child in modelClass.children :
			setattr(self, child.name, [])
		for column, meta in modelClass.meta :
			setattr(self, column, kw.get(column, meta.default))

	def toDict(self) -> dict :
		if hasattr(self, '__raw__') : return self.__raw__
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
			attribute = getattr(self, column)
			if attribute is None :
				result[column] = None
			elif meta != self :
				result[column] = meta.toDict(attribute)
		self.__raw__ = result
		return result 

	def fromDict(self, data:dict, isID:bool=False) :
		modelClass = self.__class__
		for child in modelClass.children :
			raw = data.get(child.name, None)
			if raw is not None and isinstance(raw, list) :
				setattr(self, child.name, child.fromDict(raw))
			
		for foreignKey in modelClass.foreignKey :
			raw = data.get(foreignKey.name, None)
			if raw is not None :
				if isinstance(raw, dict) :
					setattr(self, foreignKey.name, foreignKey.fromDict(raw))
				else : setattr(self, foreignKey.name, int(raw))

		for column, meta in modelClass.meta :
			raw = data.get(column, None)
			if data is None :
				setattr(self, column, None)
			elif meta.foreignKey is None and isinstance(raw, dict) :
				setattr(self, column, meta.fromDict(raw))
			elif meta.foreignKey is None:
				setattr(self, column, meta.fromDict(data))
		if isID :
			self.id = data.get(modelClass.primary, 0)
		return self
	
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
		pass
		
	@staticmethod
	def setVendor(modelClass, vendor) :
		modelClass.vendor = vendor
		for column, meta in modelClass.meta :
			meta.vendor = vendor
	
	@staticmethod
	def extractInput(modelClass) :
		order = 1
		inputList:List[Input] = []
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if not isinstance(attribute, Column) : continue
			input:Input = attribute.input
			if input is None : continue
			if input.order is None :
				input.order = f'{order}.0'
				input.parsedOrder = Version(input.order)
			input.columnType = attribute.__class__.__name__
			input.columnName = i
			inputList.append(input)
			order += 1
		inputList.sort(key=lambda x : x.parsedOrder)
		modelClass.input = inputList
		modelClass.inputDict = [i.toDict() for i in inputList]

	@staticmethod
	def extractMeta(modelClass) :
		if not hasattr(modelClass, '__version__') :
			modelClass.__version__ = '1.0'
		if not hasattr(modelClass, '__is_mapper__') :
			modelClass.__is_mapper__ = False
		modelClass.isForeignChecked = False
		primaryMeta = Record.checkPrimary(modelClass)
		Record.extractAttribute(modelClass, primaryMeta)
		Record.extractChildren(modelClass)

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
		else :
			modelClass.meta = []
			return None
	
	@staticmethod
	def extractAttribute(modelClass, primaryMeta) :
		modelClass.foreignKey = []
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if isinstance(attribute, Column) :
				attribute.name = i
				if attribute.foreignKey is not None :
					attribute.foreignKey.name = i
					modelClass.foreignKey.append(attribute.foreignKey)
				if attribute.isPrimary :
					if not hasattr(modelClass, 'primary') :
						modelClass.primary = i
						primaryMeta = attribute
					elif isinstance(modelClass.primary, list) :
						modelClass.primary.append(i)
						primaryMeta.append(attribute)
					else :
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
