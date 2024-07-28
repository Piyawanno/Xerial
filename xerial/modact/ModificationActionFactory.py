from xerial.Column import Column
from xerial.modact.AddIndexModificationAction import AddIndexModificationAction
from xerial.modact.AddModificationAction import AddModificationAction
from xerial.modact.ChangeLengthModificationAction import ChangeLengthModificationAction
from xerial.modact.ChangeTypeModificationAction import ChangeTypeModificationAction
from xerial.modact.DropIndexModificationAction import DropIndexModificationAction
from xerial.modact.DropModificationAction import DropModificationAction
from xerial.modact.ModificationAction import ModificationAction
from xerial.modact.RenameModificationAction import RenameModificationAction
from xerial.ModificationType import ModificationType


class ModificationActionFactory:
	@staticmethod
	def create(
			table: str,
			version: str,
			modificationType: ModificationType,
			columnName: str,
			column: Column,# | None,
			*args
	) -> ModificationAction:
		if modificationType == ModificationType.ADD:
			return AddModificationAction(table, version, columnName, column)
		elif modificationType == ModificationType.DROP:
			return DropModificationAction(table, version, columnName, column)
		elif modificationType == ModificationType.RENAME:
			return RenameModificationAction(table, version, columnName, column, *args)
		elif modificationType == ModificationType.CHANGE_TYPE:
			return ChangeTypeModificationAction(table, version, columnName, column, *args)
		elif modificationType == ModificationType.CHANGE_LENGTH:
			return ChangeLengthModificationAction(table, version, columnName, column)
		elif modificationType == ModificationType.ADD_INDEX:
			return AddIndexModificationAction(table, version, columnName, column)
		elif modificationType == ModificationType.DROP_INDEX:
			return DropIndexModificationAction(table, version, columnName, column)
		else:
			raise ValueError(f'Unknown modification type: {modificationType.name}')
