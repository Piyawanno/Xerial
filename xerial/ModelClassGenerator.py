from xerial.Record import Record
from xerial.Column import Column
from xerial.ColumnType import ColumnType
from xerial.input.InputType import InputType

from typing import Dict, List

class ModelClassGenerator :
	def __init__(self) :
		self.mapped:Dict[str, Record] = {}
	
	def append(self, name:str, attributeList:List[dict]) -> type :
		attributeMap = {}
		for i in attributeList :
			attributeName = i['name']
			attributeMap[attributeName] = self.createColumn(i)
		modelClass = type(name, (Record, ), attributeMap)
		self.mapped[name] = modelClass
		return modelClass
	
	def createColumn(self, attribute:dict) -> Column :
		type = attribute['type']
		columnClass = ColumnType.mapped[type]
		input = attribute.get('input', None)
		if input is not None :
			inputType = input['type']
			inputClass = InputType.mapped[inputType]
			del input['type']
			attribute['input'] = inputClass(**input)
		del attribute['type']
		del attribute['name']
		column = columnClass(**attribute)
		return column
	
	def get(self, name:str) -> type :
		return self.mapped.get(name, None)

if __name__ == '__main__' :
	generator = ModelClassGenerator()
	attributeList = [
		{
			'name' : 'name',
			'type' : ColumnType.STRING,
			'length' : 128,
			'input' : {
				'type' : InputType.TEXT,
				'label' : 'name',
				'isTable' : True,
				'isSearch' : True,
			}
		},
		{
			'name' : 'age',
			'type' : ColumnType.INTEGER,
			'isIndex' : True,
			'input' : {
				'type' : InputType.NUMBER,
				'label' : 'age',
				'isTable' : True,
				'isSearch' : True,
			}
		}
	]
	Human = generator.append('Human', attributeList)
	# RollPaper = {
	# 	'name' : 'typeRecordID',
	# 	'type' : ColumnType.INTEGER,
	# 	'isIndex' : True
	# },
	# {
	# 	'name' : 'isDrop',
	# 	'type' : ColumnType.INTEGER,
	# 	'isIndex' : True
	# }