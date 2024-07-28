import inspect
from typing import List, Dict

from xerial.Column import Column
from xerial.Input import Input
from xerial.InputExtractor import InputExtractor
from xerial.MetaDataExtractor import MetaDataExtractor
from xerial.Modification import Modification
from xerial.ModificationType import ModificationType
from xerial.Vendor import Vendor
from xerial.exception.ModificationException import ModificationException
from xerial.modact.ModificationAction import ModificationAction

__MAPPED_META__ = {}
__DEFAULT_BACKUP__ = False
__INJECTED_COLUMN__ = {}


def __getParentTableName__(modelClass):
	hierarchy = list(inspect.getmro(modelClass))
	for parent in hierarchy[1:]:
		if hasattr(parent, '__table_name__'):
			return parent.__table_name__
	return None

def __getParentFullTableName__(modelClass):
	hierarchy = list(inspect.getmro(modelClass))
	for parent in hierarchy[1:]:
		if hasattr(parent, '__full_table_name__'):
			return parent.__full_table_name__
	return None

class Record:
	def __init__(self, **kw):
		modelClass = self.__class__
		if not hasattr(modelClass, 'meta'):
			Record.extractMeta(modelClass)
		self.initRelation(**kw)

	def initRelation(self, **kw):
		modelClass = self.__class__
		for child in modelClass.children:
			setattr(self, child.name, [])
		for column, meta in modelClass.meta:
			setattr(self, column, kw.get(column, meta.default() if callable(meta.default) else meta.default))

	def toOption(self):
		modelClass = self.__class__
		avatar = {}
		modelClassAvatar = getattr(modelClass, '__avatar__', None)
		if modelClassAvatar is not None:
			avatar.update(modelClassAvatar)
			# if hasattr(self, modelClassAvatar['column'], None):
			if hasattr(self, modelClassAvatar['column']) and not getattr(self, modelClassAvatar['column']) is None:
				avatar['url'] = modelClassAvatar['url'] + getattr(self, modelClassAvatar['column'])
		return {
			'value': getattr(self, self.primaryMeta.name),
			'label': getattr(self, self.representativeMeta.name),
			'avatar': avatar
		}

	def toDict(self) -> dict:
		result = {}
		modelClass = self.__class__
		for child in modelClass.children:
			children = getattr(self, child.name)
			if isinstance(children, list):
				result[child.name] = [i.toDict() for i in children]

		for foreignKey in modelClass.foreignKey:
			linked = getattr(self, foreignKey.name)
			if isinstance(linked, Record) and linked != self:
				if not hasattr(linked, '__raw__'):
					linked.__raw__ = linked.toDict()
				result[foreignKey.name] = linked.__raw__

		for column, meta in self.meta:
			if column == '__insert_time__': continue
			if column == '__update_time__': continue
			attribute = getattr(self, column)
			if attribute is None:
				result[column] = None
			elif meta != self:
				result[column] = meta.toDict(attribute() if callable(attribute) else attribute)
		result['__avatar__'] = getattr(modelClass, '__avatar__', None)
		return result

	def setAsChildrenOf(self):
		return None

	def inject(self):
		"""
		A placeholder method for Column Injection into other model.
		By calling DBSession.appendModel(), this method will be called.
		The targeted model must be appended to DBSession before the injecting model.
		By injected column into the targeted model, column will be
		added to the model, and table structure in DB will be altered.
		Each column can be injected by calling self.injectInto method.
		"""
		pass

	def injectInto(self, targetClassName: str, columnName: str, column: Column):
		column.name = columnName
		columnMap = __INJECTED_COLUMN__.get(targetClassName, {})
		if len(columnMap) == 0: __INJECTED_COLUMN__[targetClassName] = columnMap
		columnMap[columnName] = column

	@staticmethod
	def getInjectedColumn(modelName: str) -> Dict[str, Column]:
		return __INJECTED_COLUMN__.get(modelName, {})

	@staticmethod
	def hasMeta(modelClass):
		hasMeta = hasattr(modelClass, 'meta')
		mapped = modelClass in __MAPPED_META__
		if hasMeta and not mapped: hasMeta = False
		return hasMeta
	
	@staticmethod
	def hasDocumentExport():
		return False
	
	# NOTE Proceed document export to a file and return document URL without rootURL.
	def exportDocument(self) -> str:
		raise NotImplementedError

	def toRawDict(self) -> dict:
		result = {}
		for column, meta in self.meta:
			attribute = getattr(self, column)
			if attribute is None:
				result[column] = None
			elif meta != self:
				result[column] = meta.toDict(attribute)
		return result

	def fromDict(self, data: dict, isID: bool = False):
		modelClass = self.__class__
		for child in modelClass.children:
			raw = data.get(child.name, None)
			if raw is not None:
				if isinstance(raw, list):
					setattr(self, child.name, child.fromDict(raw))
				elif isinstance(raw, dict):
					setattr(self, child.name, child.fromDict(raw.values()))

		for foreignKey in modelClass.foreignKey:
			raw = data.get(foreignKey.name, None)
			if raw is not None:
				if isinstance(raw, dict):
					setattr(self, foreignKey.name, foreignKey.fromDict(raw))
				else:
					setattr(self, foreignKey.name, foreignKey.parent.parseValue(raw))

		meta: Column
		for column, meta in modelClass.meta:
			if column not in data: continue
			raw = data[column]
			if meta.foreignKey is None and isinstance(raw, dict):
				setattr(self, column, meta.fromDict(raw))
			elif meta.foreignKey is None:
				setattr(self, column, meta.fromDict(data))
		if isID:
			self.id = data.get(modelClass.primary, 0)
		return self

	def fromRawDict(self, data: dict):
		modelClass = self.__class__
		for column, meta in modelClass.meta:
			raw = data.get(column, None)
			if data is None:
				setattr(self, column, None)
			else:
				setattr(self, column, meta.fromDict(data))

	def dereference(self):
		modelClass = self.__class__
		for foreignKey in modelClass.foreignKey:
			linked = getattr(self, foreignKey.name)
			if linked is None: continue
			if isinstance(linked, Record):
				setattr(self, foreignKey.name, getattr(linked, foreignKey.model.primary))

	def copy(self, other):
		for column, meta in self.meta:
			if hasattr(other, column):
				setattr(self, column, getattr(other, column))
		return self

	def createModification(self, version: str):
		"""
		Create a Modification object to modify Structure of Model.

		Parameters
		----------
		version: String of the new version of modification e.g. '2.0'.
		"""
		modelClass = self.__class__
		if not hasattr(modelClass, '__modification__'):
			modelClass.__modification__ = []
		modification = Modification(
			version,
			modelClass.__full_table_name__,
			modelClass.meta,
			modelClass.vendor
		)
		modelClass.__modification__.append(modification)
		return modification

	def getScopedModification(self, destination: str) -> List[Modification]:
		return [
			modification
			for modification
			in reversed(getattr(self.__class__, '__modification__', []))
			if modification.version.__str__() > destination
		]

	def getLatestModification(self) -> Modification:# | None:
		modifications: List[Modification] = getattr(self.__class__, "__modification__", [])

		if not modifications:
			return None

		latest = sorted(
			modifications,
			key=lambda modification: modification.version.__str__(),
			reverse=True
		)[0]

		return latest if modifications else None

	def createCheckout(self, modificationVersion: str, destination: str, skip: List[str] = None) -> None:
		reversedModification = self.createModification(modificationVersion)
		for existingModification in self.getScopedModification(destination):
			for action in existingModification.column:
				skipKey = action.__str__()
				if skip is not None and skipKey in skip or action.modificationType == ModificationType.CHANGE_LENGTH:
					# Also implicitly skip CHANGE_LENGTH
					if existingModification.skipped.get(modificationVersion) is None:
						existingModification.skipped[modificationVersion] = []
					existingModification.skipped[modificationVersion].append(action)
					continue

				reversedModification.reverse(action)

	def modify(self):
		"""
		A placeholder method for Structure Modification. By calling
		DBSession.checkModification(), this method of each Model
		registered to the DBSession will be called. To implement
		Structure Modification, this method must be overridden
		by creating Modification object with the method
		Record.createModification()
		"""
		pass

	def setAsChildrenOf(self):
		return None

	@staticmethod
	def hasMeta(modelClass):
		hasMeta = hasattr(modelClass, 'meta')
		mapped = modelClass in __MAPPED_META__
		if hasMeta and not mapped: hasMeta = False
		return hasMeta

	@staticmethod
	def setVendor(modelClass, vendor):
		modelClass.vendor = vendor
		for column, meta in modelClass.meta:
			meta.vendor = vendor

		if modelClass.vendor == Vendor.POSTGRESQL:
			modelClass.__table_name__ = modelClass.__table_name__.lower()
			modelClass.__full_table_name__ = modelClass.__full_table_name__.lower()

	@staticmethod
	def extractInput(modelClass, extendedInput: List[Input] = []):
		extractor = InputExtractor(modelClass, extendedInput)
		extractor.extract()

	@staticmethod
	def extractMeta(modelClass):
		extractor = MetaDataExtractor(modelClass)
		extractor.extract()
		__MAPPED_META__[modelClass] = modelClass.meta

	@staticmethod
	def checkTableName(modelClass, prefix: str):
		hasTableName = hasattr(modelClass, '__table_name__')
		parentTableName = __getParentTableName__(modelClass)
		if not hasTableName or parentTableName == modelClass.__table_name__:
			modelClass.__table_name__ = f"{prefix}{modelClass.__name__}"
		tableName = modelClass.__table_name__
		if prefix is not None and len(prefix):
			if tableName[:len(prefix)] != prefix:
				modelClass.__table_name__ = f"{prefix}{tableName}"
		hasFullName = hasattr(modelClass, '__full_table_name__')
		parentFullName = __getParentFullTableName__(modelClass)
		if not hasFullName or parentFullName == modelClass.__full_table_name__:
			hasPrefix = False
			if prefix is not None and len(prefix):
				if modelClass.__table_name__[:len(prefix)] != prefix:
					modelClass.__full_table_name__ = f"{prefix}{modelClass.__table_name__}"
					hasPrefix = True
			if not hasPrefix:
				modelClass.__full_table_name__ = modelClass.__table_name__

	@staticmethod
	def enableDefaultBackup():
		global __DEFAULT_BACKUP__
		__DEFAULT_BACKUP__ = True

	@staticmethod
	def appendGroup(modelClass, label: str, value: int, order: str, attachedGroup: str = None):
		if not hasattr(modelClass, '__addition_group__'):
			modelClass.__addition_group__ = {}
		modelClass.__addition_group__[value] = {
			'id': value,
			'label': label,
			'order': order,
			'isGroup': True,
			'attachedGroup': attachedGroup,
		}

	@staticmethod
	def mergeGroup(modelClass, group, attachedGroup: str = None):
		if not hasattr(modelClass, '__addition_group__'):
			modelClass.__addition_group__ = {}
		for i in group:
			Record.appendGroup(modelClass, group.label[i], i, group.order[i], attachedGroup)

	@staticmethod
	def disableInput(modelClass, columnName: str):
		column = getattr(modelClass, columnName, None)
		if column is None: return
		if not hasattr(column, 'input'): return
		column.input = None

	@staticmethod
	def replaceInput(modelClass, columnName: str, input: Input):
		column = getattr(modelClass, columnName, None)
		if column is None: return
		if not hasattr(column, 'input'): return
		column.input = input

	@staticmethod
	def analyzeModifications(modifications: List[Modification]) -> Dict[str, List[ModificationException]]:
		modificationExceptions: Dict[str, List[ModificationException]] = {}
		for modification in modifications:
			exceptions = modification.analyze()
			if len(exceptions) > 0:
				modificationExceptions[modification.version] = exceptions
		return modificationExceptions

	@staticmethod
	def getSkippedActions(modifications: List[Modification]) -> Dict[str, List[ModificationAction]]:
		skippedActions: Dict[str, List[ModificationAction]] = {}
		for modification in modifications:
			actions = modification.getSkippedActions()
			if len(actions) > 0:
				skippedActions[modification.version] = actions
		return skippedActions
