from typing import Dict
from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from xerial.Filter import Filter

class SliderInput (Input):
	def __init__(
			self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			isAdvanceForm:bool=False,
			isTableForm:bool=False,
			isView:bool=False,
			isSearchTable:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			linkColumn:str='',
			help:str=None,
			isNegative:bool=True,
			isZeroIncluded:bool=True,
			isFloatingPoint:bool=True,
			minValue:float=None,
			maxValue:float=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
			sideIcon:str=None,
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
			isCopyable:bool=False,
			inputPerLine:int=None,
			filter: Filter=None,
			placeHolder:str=None,
			typeName:str = 'Slider',
		) :
		Input.__init__(
			self,
			label,
			order,
			group,
			isTable,
			isMobile,
			isSearch,
			isRequired,
			isEditable,
			isForm,
			isAdvanceForm,
			isTableForm,
			isView,
			isSearchTable,
			attachedGroup,
			isLink,
			linkColumn,
			help,
			documentPath,
			config,
			columnType,
			columnName,
			sideIcon,
			isEnabled,
			isSpreadSheet,
			isCopyable,
			inputPerLine,
			filter,
			placeHolder,
			typeName,
		)
		self.isNegative = isNegative
		self.isZeroIncluded = isZeroIncluded
		self.isFloatingPoint = isFloatingPoint
		self.minValue=minValue
		self.maxValue=maxValue
		self.isNumber = True

	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isNegative'] = self.isNegative
		data['isZeroIncluded'] = self.isZeroIncluded
		data['isFloatingPoint'] = self.isFloatingPoint
		data['minValue'] = self.minValue() if callable(self.minValue) else self.minValue
		data['maxValue'] = self.maxValue() if callable(self.maxValue) else self.maxValue
		return data
