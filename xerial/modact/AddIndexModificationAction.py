from xerial.Column import Column
from xerial.modact.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class AddIndexModificationAction(ModificationAction):
	def __init__(self, table: str, version: str, name: str, column: Column) -> None:
		super().__init__(table, version, ModificationType.ADD_INDEX, name, column)

	def reverseArgs(self) -> tuple:
		return self.columnName,

	def verbose(self) -> str:
		return f'Add index {self.columnName} to {self.table}'
