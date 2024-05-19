from xerial.Column import Column
from xerial.JSONColumn import JSONColumn
from xerial.Input import Input
from xerial.InputGroupEnum import InputGroupEnum

from typing import List, Dict
from packaging.version import Version
from enum import IntEnum

import copy

class InputExtractor :
	def __init__(self, modelClass, extendedInput) :
		self.modelClass = modelClass
		self.extendedInput = extendedInput
	
	def extract(self) :
		self.inputPerLine = getattr(self.modelClass, 'inputPerLine', 2)
		self.inputList:List[Dict] = []
		self.modelClass.__file_input__ = []
		self.mergedInput:List[Input] = self.extractBase()
		self.mergedInput.extend(self.extendedInput)
		self.extractAttached()
		self.groupedInputList = []
		self.inputGroupMapper:Dict[int, List[Input]] = {}
		self.checkOrder()
		self.checkGroup()
		self.modelClass.__has_callable_default__ = self.checkDefault()
		self.inputList.sort(key=lambda x : x['parsedOrder'])
		self.extractGroupInput()
		self.groupedInputList.sort(key=lambda x : x['parsedOrder'])
		self.modelClass.input = []
		self.removeParsedOrder()
		# self.sortAttachedGroup()
		self.modelClass.inputDict = self.inputList
	
	def sortAttachedGroup(self) :
		attachedGroup = []
		for attached in self.modelClass.attachedGroup.values() :
			attached['parsedOrder'] = Version(attached['order'])
			attachedGroup.append(attached)
		attachedGroup.sort(key=lambda x : x['parsedOrder'])
		for attached in attachedGroup :
			del attached['parsedOrder']
		self.modelClass.attachedGroup = attachedGroup
	
	def removeParsedOrder(self) :
		for item in self.groupedInputList:
			del item['parsedOrder']
			self.modelClass.input.append(item)
		for item in self.inputList:
			if 'parsedOrder' in item: del item['parsedOrder']
	
	def checkDefault(self) :
		hasDefaultCallable = False
		for i, input in zip(self.mergedInput, self.inputList) :
			default = getattr(i.attribute, 'default', None)
			if not hasDefaultCallable : hasDefaultCallable = callable(default)
			input['default'] = default
		return hasDefaultCallable
			
	def checkOrder(self) :
		order = 1
		for i in self.mergedInput :
			inputPerLine = self.inputPerLine
			inputPerLineEach = getattr(i, 'inputPerLine', None)
			if not inputPerLineEach is None: inputPerLine = inputPerLineEach
			input:Dict = i.toDict()
			if not 'order' in input or input['order'] is None:
				input['order'] = f'{order}.0'
			input['parsedOrder'] = Version(input['order'])
			input['isGroup'] = False
			input['inputPerLine'] = inputPerLine
			self.inputList.append(input)
			order += 1
	
	def checkGroup(self) :
		for i, input in zip(self.mergedInput, self.inputList) :
			if i.group is None: 
				self.groupedInputList.append(copy.copy(input))
				continue
			value = i.group if isinstance(i.group, int) else i.group.value
			if not value in self.inputGroupMapper:
				self.inputGroupMapper[value] = []
			self.inputGroupMapper[value].append(input)
	
	def extractBase(self) :
		inputList:List[Input] = []
		inputList.extend(self.extractChildrenInput())
		for i, attribute in self.modelClass.meta :
			if not isinstance(attribute, Column) : continue
			if attribute.input is None : continue
			if not attribute.input.isEnabled: continue
			attribute.input.columnType = attribute.__class__.__name__
			attribute.input.columnName = i
			if attribute.isRepresentative:
				attribute.input.isLink = True
				attribute.input.linkColumn = 'id'
			if not attribute.foreignKey is None:
				attribute.input.foreignModelName = attribute.foreignKey.modelName
				attribute.input.foreignColumn = attribute.foreignKey.column
			if isinstance(attribute, JSONColumn) and hasattr(attribute.input, 'setOrderAttribute'):
				attribute.input.setOrderAttribute(attribute)
			inputList.append(attribute.input)
			if getattr(attribute.input, 'isFile', False) :
				self.modelClass.__file_input__.append(attribute.input)
		return inputList
	
	def extractChildrenInput(self):
		from xerial.Children import Children
		item:Children
		inputList:List[Input] = []
		for item in self.modelClass.children:
			if item.input is None: continue
			if not item.input.isEnabled: continue
			column:Column = item.model.metaMap.get(item.name, None)
			item.input.columnName = item.name
			item.input.columnType = column.__class__.__name__
			item.input.foreignModelName = column.foreignKey.modelName
			item.input.foreignColumn = column.foreignKey.column
			item.input.childrenModelName = item.model.__name__
			inputList.append(item.input)
		return inputList
	
	def extractGroupInput(self) :
		self.groupParsedOrder = []
		self.extractGroupLabel()
		self.extractAdditionGroup()
		self.groupParsedOrder.sort(key=lambda x : x['parsedOrder'])
		filterValue = lambda i : {'id': i['id'], 'label': i['label'], 'order': i['order']}
		self.groupParsedOrder = [filterValue(i) for i in self.groupParsedOrder]
		self.modelClass.inputGroup = self.groupParsedOrder
	
	def extractAttached(self) :
		self.modelClass.attachedGroup = {}
		for i in self.mergedInput :
			attached = i.attachedGroup
			if attached is None : continue
			i.attachedGroupID = attached.ID
			if attached.ID not in self.modelClass.attachedGroup :
				self.modelClass.attachedGroup[attached.ID] = attached.toDict()
	
	def groupInput(self, parsedOrder) :
		if parsedOrder['id'] in self.inputGroupMapper:
			self.inputGroupMapper[parsedOrder['id']].sort(key=lambda x : x['parsedOrder'])
			parsedOrder['input'] = []
			for item in self.inputGroupMapper[parsedOrder['id']]:
				del item['parsedOrder']
				parsedOrder['input'].append(item)

		self.groupedInputList.append(parsedOrder)
		self.groupParsedOrder.append(parsedOrder)
	
	def extractGroupLabel(self) :
		group:IntEnum = getattr(self.modelClass, '__group_label__', None)
		isInputGroup = issubclass(group, InputGroupEnum) if group is not None else False
		if group is None : return
		inputPerLine = getattr(self.modelClass, 'inputPerLine', 2)
		attachedGroup = getattr(group, 'attachedGroup', {})
		if isInputGroup:
			for i in group :
				inputPerLineEach = getattr(i.item, 'inputPerLine', None)
				if not inputPerLineEach is None: inputPerLine = inputPerLineEach
				parsedOrder = {
					'id': i.value,
					'label': i.item.label,
					'order': i.item.order,
					'isGroup': True,
					'inputPerLine': inputPerLine,
					'attachedGroup': attachedGroup.get(i.value, None),
					'parsedOrder': Version(i.item.order)
				}
				self.groupInput(parsedOrder)
		else :
			for i in group.order:
				inputPerLineEach = getattr(i, 'inputPerLine', None)
				if not inputPerLineEach is None: inputPerLine = inputPerLineEach
				parsedOrder = {
					'id': i.value,
					'label': i.label[i],
					'order': group.order[i],
					'isGroup': True,
					'inputPerLine': inputPerLine,
					'attachedGroup': attachedGroup.get(i, None),
				}
				parsedOrder['parsedOrder'] = Version(group.order[i])
				self.groupInput(parsedOrder)
	
	def extractAdditionGroup(self) :
		addition = getattr(self.modelClass, '__addition_group__', None)
		if addition is None : return
		inputPerLine = getattr(self.modelClass, 'inputPerLine', 2)
		for i in addition.values() :
			inputPerLineEach = getattr(i, 'inputPerLine', None)
			if not inputPerLineEach is None: inputPerLine = inputPerLineEach
			i['parsedOrder'] = Version(i['order'])
			i['inputPerLine'] = inputPerLine
			self.groupInput(i)