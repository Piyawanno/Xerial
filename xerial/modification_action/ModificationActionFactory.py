from xerial.Column import Column
from xerial.modification_action.AddIndexModificationAction import AddIndexModificationAction
from xerial.modification_action.AddModificationAction import AddModificationAction
from xerial.modification_action.ChangeLengthModificationAction import ChangeLengthModificationAction
from xerial.modification_action.ChangeTypeModificationAction import ChangeTypeModificationAction
from xerial.modification_action.DropIndexModificationAction import DropIndexModificationAction
from xerial.modification_action.DropModificationAction import DropModificationAction
from xerial.modification_action.ModificationAction import ModificationAction
from xerial.modification_action.RenameModificationAction import RenameModificationAction
from xerial.ModificationType import ModificationType


class ModificationActionFactory:
    @staticmethod
    def create(
            table: str,
            version: str,
            modificationType: ModificationType,
            columnName: str,
            column: Column | None,
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
