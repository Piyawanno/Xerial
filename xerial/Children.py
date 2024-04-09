from xerial.FormComponent import FormComponent
from xerial.Input import Input

class Children :
	def __init__(
			self,
			reference:str,
			isTableForm:bool=False,
			isSearchTable:bool=False,
			title:str='',
			formComponent: FormComponent=None,
			input: Input=None,
		) :
		self.reference = reference
		splitted = reference.split(".")
		self.modelName = splitted[0]
		self.column = splitted[1]
		self.isTableForm = isTableForm
		self.isSearchTable = isSearchTable
		self.parentColumn = None
		self.formComponent = formComponent
		self.input = input
		self.name = None
		self.model = None
		self.title = title

	def fromDict(self, data:list) :
		return [self.model().fromDict(i) for i in data]
	
	def toMetaDict(self) :
		return {
			'reference': self.reference,
			'modelName': self.modelName,
			'column': self.column,
			'isTableForm': self.isTableForm,
			'isSearchTable': self.isSearchTable,
			'parentColumn': self.parentColumn,
			'formComponent': None if self.formComponent is None else self.formComponent.extract(self.modelName),
			'input': None if self.input is None else self.input.toDict(),
			'name': self.name,
			'title': self.title
		}