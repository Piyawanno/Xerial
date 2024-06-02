from typing import List

from xerial.Column import Column
from xerial.exception.ModificationException import ModificationException
from xerial.ModificationType import ModificationType


class ModificationAction:
	def __init__(
			self,
			table: str,
			version: str,
			modificationType: ModificationType,
			columnName: str,
			column: Column
	) -> None:
		self.table = table
		self.version = version
		self.modificationType = modificationType
		self.columnName = columnName
		self.column = column

	def prefix(self) -> str:
		return (
			f'{self.table}-'
			f'{self.version}-'
			f'{self.modificationType.name}-'
			f'{self.columnName}'
		)

	def baseTuple(self) -> tuple:
		return self.table, self.columnName

	def __str__(self) -> str:
		return self.prefix()

	def tuple(self) -> tuple:
		return self.baseTuple()

	def reverseArgs(self) -> tuple:
		raise NotImplementedError('This method must be overridden in a subclass.')

	def analyze(self) -> List[ModificationException]:
		return []

	def verbose(self) -> str:
		return self.prefix()
