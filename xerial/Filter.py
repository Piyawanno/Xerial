
from typing import List, Dict

from xerial.FilterOperation import FilterOperation

class Filter :
	def __init__(self, operations: List[FilterOperation] = [], typeName:str=None) -> None:
		self.operations = operations
		self.typeName = typeName

	def toDict(self) -> Dict:
		return {
			"typeName": self.typeName,
			"operations": [{'value': i.value, 'label': FilterOperation.sign[i]} for i in self.operations]
		}
	