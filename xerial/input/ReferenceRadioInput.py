from typing import Dict
from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class ReferenceRadioInput (ReferenceSelectInput) :
	def __init__(self,
			label:str,
			url:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
			documentPath:str=None,
			config:Dict=None
		) :
		ReferenceSelectInput.__init__(
			label,
			url,
			order,
			group,
			isTable,
			isMobile,
			isSearch,
			isRequired,
			isEditable,
			help,
			documentPath,
			config
		)
		self.typeName = 'ReferenceRadio'