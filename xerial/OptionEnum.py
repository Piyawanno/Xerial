import enum
from typing import Dict

class OptionItem:
	def __init__(
			self,
			value: int,
			label: str,
			color: str='',
			icon: str='',
		):
		self.value = value
		self.label = label
		self.color = color
		self.icon = icon
	
	def toDict(self):
		return {
			'value': self.value,
			'label': self.label,
			'color': self.color,
			'icon': self.icon,
		}
		

class OptionEnum (enum.Enum):
	@classmethod
	def getColorMap(klass) -> Dict[int, str]:
		if not hasattr(klass, 'colorMap'):
			klass.colorMap = {}
			for i in klass:
				klass.colorMap[i.value] = i.color
		return klass.colorMap
	
	@classmethod
	def getLabelMap(klass) -> Dict[int, str]:
		if not hasattr(klass, 'labelMap'):
			klass.labelMap = {}
			for i in klass:
				klass.labelMap[i.value] = i.label
		return klass.labelMap

	@classmethod
	def getIconMap(klass) -> Dict[int, str]:
		if not hasattr(klass, 'iconMap'):
			klass.iconMap = {}
			for i in klass:
				klass.iconMap[i.value] = i.icon
		return klass.iconMap

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
	def icon(self):
		return super().value.icon
	
	@property
	def label(self):
		return super().value.label
	
	@classmethod
	def toDict(enumClass):
		return [i.item.toDict() for i in enumClass]
	
	@classmethod
	def toClass(enumClass):
		return [i.item for i in enumClass]
	