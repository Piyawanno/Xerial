from xerial.Input import Input

class NumberInput (Input):
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
			isNegative:bool=True,
			isZeroIncluded:bool=True,
			isFloatingPoint:bool=True,
			maxValue:float=None,
			documentPath:str=None,
		) :
		Input.__init__(
			self,
			label,
			order,
			group,
			isTable,
			isSearch,
			isRequired,
			isEditable,
			help,
			documentPath
		)
		self.typeName = 'Number'
		self.isNegative = isNegative
		self.isZeroIncluded = isZeroIncluded
		self.isFloatingPoint = isFloatingPoint
		self.maxValue=maxValue

	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isNegative'] = self.isNegative
		data['isZeroIncluded'] = self.isZeroIncluded
		data['isFloatingPoint'] = self.isFloatingPoint
		data['maxValue'] = self.maxValue
		return data
