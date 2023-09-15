from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from xerial.input.SelectInput import SelectInput

from typing import Dict, List, Tuple

class RadioInput (SelectInput):
	def __init__(self,
			label:str,
			option:List[Tuple[int, str]],
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
			attachedGroup:InputAttachment=None,
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
		) :
		SelectInput.__init__(
			self,
			label,
			option,
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
		self.typeName = 'Radio'

