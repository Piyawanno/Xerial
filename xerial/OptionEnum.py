import enum


class OptionItem:
	def __init__(
			self,
			value: int,
			label: str,
			color: str='',
		):
		self.value = value
		self.label = label
		self.color = color
	
	def toDict(self):
		return {
			'value': self.value,
			'label': self.label,
			'color': self.color,
		}
		

class OptionEnum (enum.Enum):
	@property
	def item(self):
		return super().value
	
	@property
	def value(self):
		return super().value.value
	
	@property
	def color(self):
		return super().value.color
	
	@property
	def label(self):
		return super().value.label
	
	@classmethod
	def toDict(enumClass):
		return [i.item.toDict() for i in enumClass]
	
	@classmethod
	def toClass(enumClass):
		return [i.item for i in enumClass]
	