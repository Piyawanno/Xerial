from xerial.Column import Column
from xerial.Input import Input

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
		self.mergedInput:List[Input] = self.extractBase()
		self.mergedInput.extend(self.extendedInput)
		self.extractAttached()
		self.groupedInputList = []
		self.inputGroupMapper:Dict[int, List[Input]] = {}
		self.modelClass.fileInput = []
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
			input:Dict = i.toDict()
			if not 'order' in input or input['order'] is None:
				input['order'] = f'{order}.0'
			input['parsedOrder'] = Version(input['order'])
			input['isGroup'] = False
			input['inputPerLine'] = self.inputPerLine
			self.inputList.append(input)
			order += 1
	
	def checkGroup(self) :
		for i, input in zip(self.mergedInput, self.inputList) :
			if i.group is None: 
				self.groupedInputList.append(copy.copy(input))
				continue
			if not i.group in self.inputGroupMapper:
				self.inputGroupMapper[i.group] = []
			self.inputGroupMapper[i.group].append(input)
	
	def extractBase(self) :
		inputList = []
		for i, attribute in self.modelClass.meta :
			if not isinstance(attribute, Column) : continue
			if attribute.input is None : continue
			attribute.input.columnType = attribute.__class__.__name__
			attribute.input.columnName = i
			inputList.append(attribute.input)
			if getattr(attribute, 'isFile', False) :
				self.modelClass.fileInput.append(attribute)
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
		if group is None : return
		inputPerLine = getattr(self.modelClass, 'inputPerLine', 2)
		attachedGroup = getattr(group, 'attachedGroup', {})
		for i in group.order:
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
			i['parsedOrder'] = Version(i['order'])
			i['inputPerLine'] = inputPerLine
			self.groupInput(i)