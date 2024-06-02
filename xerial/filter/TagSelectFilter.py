from typing import List
from xerial.Filter import Filter
from xerial.FilterOperation import FilterOperation

class TagSelectFilter (Filter):
	def __init__(self, operations: List[FilterOperation] = None, typeName: str = "TagSelect") -> None:
		if operations is None: operations = self.getFilterOperation()
		super().__init__(operations, typeName)

	def getFilterOperation(self) -> List[FilterOperation]:
		return [
			FilterOperation.EQUAL,
			FilterOperation.NOT_EQUAL,
			FilterOperation.IN,
			FilterOperation.NOT_IN
		]