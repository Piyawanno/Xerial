class InputAttachment :
	def __init__(self, ID:str, label:str, order:str, isEnabled:bool=False) :
		self.ID = ID
		self.label = label
		self.order = order
		self.isEnabled = isEnabled
	
	def toDict(self) :
		return {
			'ID': self.ID,
			'label': self.label,
			'order': self.order,
			'isEnabled': self.isEnabled,
		}