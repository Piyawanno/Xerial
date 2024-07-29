from xerial.Column import Column
from xerial.Children import Children

import logging

__RESERVED__ = {
	'meta',
	'primaryMeta',
	'primitive',
	'representativeMeta',
	'__full_table_name__',
	'__table_name__',
	'__generated_index__',
	'__is_created__',
}

class MetaDataExtractor :
	def __init__(self, modelClass):
		self.modelClass = modelClass
	
	def extract(self) :
		modelClass = self.modelClass
		self.checkDefault()
		modelClass.representativeMeta = None
		modelClass.isForeignChecked = False
		modelClass.hasChildrenChecked  = False
		primaryMeta = self.getPrimary()
		MetaDataExtractor.checkBackup(self.modelClass)
		self.extractAttribute(primaryMeta)
		self.extractChildren()
		modelClass.metaMap = {k:v for k, v in modelClass.meta}
	
	def getPrimary(self) :
		modelClass = self.modelClass
		if not self.hasParent() :
			primaryMeta = self.extractPrimary()
		else :
			if hasattr(modelClass, '__has_primary__') and modelClass.__has_primary__ :
				primaryMeta = modelClass.primaryMeta
				modelClass.meta = [(modelClass.primary, primaryMeta)]
			else :
				primaryMeta = None
		return primaryMeta
	
	def checkDefault(self) :
		modelClass = self.modelClass
		if not hasattr(modelClass, '__version__') :
			modelClass.__version__ = '1.0'
		if not hasattr(modelClass, '__is_mapper__') :
			modelClass.__is_mapper__ = False
		if not hasattr(modelClass, '__skip_create__') :
			modelClass.__skip_create__ = False
		

	def extractChildren(self):
		modelClass = self.modelClass
		modelClass.children = []
		modelClass.hasChildrenChecked = False
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if isinstance(attribute, Children) :
				attribute.name = i
				modelClass.children.append(attribute)
	
	def extractParentForeign(self, parentMetaMap, attribute, name):
		modelClass = self.modelClass
		parentAttribute: Column = parentMetaMap[name]
		modelClass.meta.append((name, parentAttribute))
		if isinstance(parentAttribute, Column) and parentAttribute.foreignKey is not None :
			modelClass.foreignKey.append(parentAttribute.foreignKey)
	
	def extractColumn(self, attribute) :
		modelClass = self.modelClass
		if attribute.isRepresentative :
			if modelClass.representativeMeta is None :
				modelClass.representativeMeta = attribute
			else :
				logging.warning(f"Multiple representative columns are defined@{modelClass.__name__}.")
		if attribute.foreignKey is not None :
			attribute.foreignKey.name = attribute.name
			modelClass.foreignKey.append(attribute.foreignKey)
		if attribute.isPrimary :
			primaryMeta = attribute
			if not hasattr(modelClass, 'primary') :
				modelClass.primary = attribute.name
			elif isinstance(modelClass.primary, list) :
				if attribute.name not in modelClass.primary :
					modelClass.primary.append(attribute.name)
					primaryMeta.append(attribute)
			elif  modelClass.primary != attribute.name :
				modelClass.primary = [attribute.name]
				primaryMeta = [primaryMeta]
		modelClass.meta.append((attribute.name, attribute))
		setattr(modelClass, attribute.name, attribute.default)
	
	def extractAttribute(self, primaryMeta) :
		modelClass = self.modelClass
		modelClass.foreignKey = []
		parentMetaMap = getattr(modelClass, 'metaMap', {})
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if i in __RESERVED__ : continue
			if i in parentMetaMap :
				self.extractParentForeign(parentMetaMap, attribute, i)
			elif isinstance(attribute, Column) :
				attribute.name = i
				self.extractColumn(attribute)
		modelClass.metaMap = {k:v for k, v in modelClass.meta}
		if primaryMeta is not None :
			modelClass.primaryMeta = primaryMeta
	
	def hasParent(self) :
		from xerial.Record import __MAPPED_META__
		modelClass = self.modelClass
		hasMeta = hasattr(modelClass, 'meta')
		if not hasMeta : return False
		mapped = modelClass in __MAPPED_META__
		return not mapped
	
	def extractPrimary(self) :
		modelClass = self.modelClass
		from xerial.IntegerColumn import IntegerColumn
		for i in dir(modelClass) :
			attribute = getattr(modelClass, i)
			if not isinstance(attribute, Column) : continue
			if not attribute.isPrimary : continue
			modelClass.__has_primary__ = True
			modelClass.primary = i
			modelClass.meta = []
			return
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
	def checkBackup(modelClass) :
		from xerial.Record import __DEFAULT_BACKUP__
		from xerial.FloatColumn import FloatColumn
		if not hasattr(modelClass, '__backup__') : modelClass.__backup__ = __DEFAULT_BACKUP__
		if not modelClass.__backup__ : return
		modelClass.__insert_time__ = FloatColumn(isIndex=True, default=-1.0)
		modelClass.__update_time__ = FloatColumn(isIndex=True, default=-1.0)
	
	