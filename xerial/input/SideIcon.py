from typing import Dict

class SideIcon :
	def __init__(self,
		name: str,
		icon: str,
		order: str='1.0',
		label: str='',
		renderClass: str='SideIcon',
	):
		self.name = name
		self.icon = icon
		self.order = order
		self.label = label
		self.renderClass = renderClass
	
	def toDict(self) -> Dict[str, str]:
		return {
			'name': self.name,
			'icon': self.icon,
			'order': self.order,
			'label': self.label,
			'renderClass': self.renderClass,
		}