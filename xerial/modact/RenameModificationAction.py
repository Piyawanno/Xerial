from xerial.Column import Column
from xerial.modact.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class RenameModificationAction(ModificationAction):
	def __init__(self, table: str, version: str, oldName: str, column: Column, newName: str) -> None:
		super().__init__(table, version, ModificationType.RENAME, oldName, column)
		self.newName = newName

	def __str__(self) -> str:
		return f'{self.prefix()}-{self.newName}'

	def tuple(self) -> tuple:
		return self.baseTuple() + (self.newName,)

	def reverseArgs(self) -> tuple:
		return self.columnName, self.newName

	def verbose(self) -> str:
		return f'Rename {self.columnName} to {self.newName} in {self.table}'
