from xerial.Modification.ModificationActon.AddIndexModificationAction import AddIndexModificationAction
from xerial.Modification.ModificationActon.AddModificationAction import AddModificationAction
from xerial.Modification.ModificationActon.ChangeLengthModificationAction import ChangeLengthModificationAction
from xerial.Modification.ModificationActon.ChangeTypeModificationAction import ChangeTypeModificationAction
from xerial.Modification.ModificationActon.DropIndexModificationAction import DropIndexModificationAction
from xerial.Modification.ModificationActon.DropModificationAction import DropModificationAction
from xerial.Modification.ModificationActon.ModificationAction import ModificationAction
from xerial.Modification.ModificationActon.RenameModificationAction import RenameModificationAction
from xerial.ModificationType import ModificationType


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
