from typing import Dict
from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from xerial.Filter import Filter

class ImageInput (Input):
	def __init__(
			self,
			label:str,
			url:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isPreview:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			isAdvanceForm:bool=False,
			isTableForm:bool=False,
			isView:bool=False,
			isSearchTable:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			isShare:bool=False,
			linkColumn:str='',
			help:str=None,
			path:str=None,
			uploadURL:str=None,
			documentPath:str=None,
			hasCrop:bool=False,
			aspectRatio:float=1.0,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
			sideIcon:str=None,
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
			isCopyable:bool=False,
			inputPerLine:int=None,
			filter: Filter=None,
			placeHolder:str=None,
			typeName:str = 'Image',
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
			sideIcon,
			isEnabled,
			isSpreadSheet,
			isCopyable,
			inputPerLine,
			filter,
			placeHolder,
			typeName,
		)
		if len(url) and url[-1] != '/': url = url+'/'
		self.url = url
		self.isPreview = isPreview
		self.isShare = isShare
		self.path = path
		self.uploadURL = uploadURL
		self.hasCrop = hasCrop
		self.aspectRatio = aspectRatio
		self.isFile = True
	
	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isPreview'] = self.isPreview
		data['path'] = self.path
		data['uploadURL'] = self.uploadURL
		data['url'] = self.url
		data['hasCrop'] = self.hasCrop
		data['aspectRatio'] = self.aspectRatio
		data['isShare'] = self.isShare
		data['isFile'] = True
		return data