from typing import Dict
from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class ReferenceCheckBoxInput (ReferenceSelectInput) :
	def __init__(self,
			label:str,
			url:str,
			tableURL:str=None,
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
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
		) :
		ReferenceSelectInput.__init__(
			label,
			url,
			tableURL,
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
		self.typeName = 'ReferenceCheckBox'