from typing import List
from xerial.Filter import Filter
from xerial.FilterOperation import FilterOperation

class CheckBoxFilter (Filter):
	def __init__(self, operations: List[FilterOperation] = None, typeName: str = "CheckBox") -> None:
		if operations is None: operations = self.getFilterOperation()
		super().__init__(operations, typeName)

	def getFilterOperation(self) -> List[FilterOperation]:
		return [
			FilterOperation.CONTAIN,
			FilterOperation.NOT_CONTAIN
		]