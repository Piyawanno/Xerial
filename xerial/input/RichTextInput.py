from typing import Dict
from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from xerial.input.RichTextHandler import RichTextHandler
from xerial.Filter import Filter
from typing import List

class RichTextInput (Input):
	def __init__(
			self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			isAdvanceForm:bool=False,
			isTableForm:bool=False,
			isView:bool=False,
			isSearchTable:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			linkColumn:str='',
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			hasImage: bool=True,
			hasVideo: bool=True,
			hasLink: bool=True,
			handler: List[RichTextHandler]=[],
			columnType:str='',
			columnName:str='',
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
			isCopyable:bool=False,
			inputPerLine:int=None,
			filter: Filter=None,
			typeName:str = 'RichText',
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
			isAdvanceForm,
			isTableForm,
			isView,
			isSearchTable,
			attachedGroup,
			isLink,
			linkColumn,
			help,
			documentPath,
			config,
			columnType,
			columnName,
			isEnabled=isEnabled,
			isSpreadSheet=isSpreadSheet,
			isCopyable=isCopyable,
			inputPerLine=inputPerLine,
			filter=filter,
			typeName=typeName,
		)
		self.hasImage: bool = hasImage
		self.hasVideo: bool = hasVideo
		self.hasLink: bool = hasLink
		self.handler: List[RichTextHandler] = handler

	def toDict(self) -> dict:
		result = super().toDict()
		result['config'] = self.config
		result['hasImage'] = self.hasImage
		result['hasVideo'] = self.hasVideo
		result['hasLink'] = self.hasLink
		result['handler'] = [i.toDict() for i in self.handler]
		return result