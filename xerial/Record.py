from dataclasses import dataclass
from xerial.Column import Column
from xerial.Children import Children
from xerial.Input import Input
from xerial.Modification import Modification
from packaging import version
from typing import List, Type

class Record :
	def __init__(self, **kw) :
		for column, meta in self.meta :
			setattr(self, column, kw.get(column, meta.default))

	def toDict(self) -> dict:
		result = {}
		for column, meta in self.meta :
			attribute = getattr(self, column)
			if attribute is None :
				result[column] = None
			else :
				result[column] = meta.toDict(attribute)
		return result 

	def fromDict(self, data:dict, isID:bool=False) :
		for column, meta in self.meta :
			if data is None :
				setattr(self, column, None)
			else :
				setattr(self, column, meta.fromDict(data))
		if isID :
			self.id = data.get(column, 0)
		return self
	
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
				input.parsedOrder = version.parse(input.order)
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
					if len(attribute.foreignKey) != 2 :
						raise ValueError(f"Foreign key should be CLASSNAME.PrimaryKey. Check {modelClass}.{attribute.name}")
					modelClass.foreignKey.append((i, attribute.foreignKey[0], attribute.foreignKey[1]))
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
