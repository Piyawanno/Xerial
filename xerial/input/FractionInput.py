from typing import Dict
from xerial.Input import Input

class FractionInput (Input):
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			isTableForm:bool=False,
			help:str=None,
			isNegative:bool=True,
			isZeroIncluded:bool=True,
			isFloatingPoint:bool=True,
			maxValue:float=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
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
			isTableForm,
			help,
			documentPath,
			config,
			columnType,
			columnName,
		)
		self.typeName = 'Fraction'
		self.isNegative = isNegative
		self.isZeroIncluded = isZeroIncluded
		self.isFloatingPoint = isFloatingPoint
		self.maxValue=maxValue
		self.isNumber = True

	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isNegative'] = self.isNegative
		data['isZeroIncluded'] = self.isZeroIncluded
		data['isFloatingPoint'] = self.isFloatingPoint
		data['maxValue'] = self.maxValue
		return data
