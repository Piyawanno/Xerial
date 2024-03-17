from xerial.ModificationType import ModificationType
from xerial.modification.ModificationActon.AddIndexModificationAction import AddIndexModificationAction
from xerial.modification.ModificationActon.AddModificationAction import AddModificationAction
from xerial.modification.ModificationActon.ChangeLengthModificationAction import ChangeLengthModificationAction
from xerial.modification.ModificationActon.ChangeTypeModificationAction import ChangeTypeModificationAction
from xerial.modification.ModificationActon.DropIndexModificationAction import DropIndexModificationAction
from xerial.modification.ModificationActon.DropModificationAction import DropModificationAction
from xerial.modification.ModificationActon.ModificationAction import ModificationAction
from xerial.modification.ModificationActon.RenameModificationAction import RenameModificationAction


class ModificationActionFactory:
    @staticmethod
    def create(
            table: str,
            version: str,
            modification_type: ModificationType,
            column_name: str,
            *args
    ) -> ModificationAction:
        if modification_type == ModificationType.ADD:
            return AddModificationAction(table, version, column_name, *args)
        elif modification_type == ModificationType.DROP:
            return DropModificationAction(table, version, column_name, *args)
        elif modification_type == ModificationType.RENAME:
            return RenameModificationAction(table, version, column_name, *args)
        elif modification_type == ModificationType.CHANGE_TYPE:
            return ChangeTypeModificationAction(table, version, column_name, *args)
        elif modification_type == ModificationType.CHANGE_LENGTH:
            return ChangeLengthModificationAction(table, version, column_name, *args)
        elif modification_type == ModificationType.ADD_INDEX:
            return AddIndexModificationAction(table, version, column_name, *args)
        elif modification_type == ModificationType.DROP_INDEX:
            return DropIndexModificationAction(table, version, column_name, *args)
        else:
            raise ValueError(f'Unknown modification type: {modification_type.name}')
