class InputAttachment :
	def __init__(self, ID:str, label:str, value:int, isEnabled:bool=False) :
		self.ID = ID
		self.label = label
		self.value = value
		self.isEnabled = isEnabled
	
	def toDict(self) :
		return {
			'ID': self.ID,
			'label': self.label,
			'value': self.value,
			'isEnabled': self.isEnabled,
		}