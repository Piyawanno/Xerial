from typing import Dict
from xerial.Input import Input

class TextAreaInput (Input):
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
			isAdvanceFrom:bool=False,
			attachedGroup:str='',
			help:str=None,
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
			isAdvanceFrom,
			attachedGroup,
			help,
			documentPath,
			config,
			columnType,
			columnName,
		)
		self.typeName = 'TextArea'