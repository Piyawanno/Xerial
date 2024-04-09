import enum


class InputGroupItem:
	def __init__(
			self,
			value: int,
			label: str,
			order: str,
			inputPerLine:int=2,
			isEnabled: bool=True
		):
		self.value = value
		self.label = label
		self.order = order
		self.inputPerLine = inputPerLine
		self.isEnabled = isEnabled
	
	def toDict(self):
		return {
			'value': self.value,
			'label': self.label,
			'order': self.order,
			'inputPerLine': self.inputPerLine,
			'isEnabled': self.isEnabled,
		}
		

class InputGroupEnum (enum.Enum):
	@property
	def item(self):
		return super().value
	
	@property
	def value(self):
		return super().value.value
	
	@property
	def label(self):
		return super().value.label
	
	@property
	def order(self):
		return super().value.order
	
	@classmethod
	def toDict(enumClass):
		return [i.item.toDict() for i in enumClass]
	
	@classmethod
	def toClass(enumClass):
		return [i.item for i in enumClass]
	