from xerial.ModificationType import ModificationType
from xerial.modification.ModificationTuple.AddIndexModificationTuple import AddIndexModificationTuple
from xerial.modification.ModificationTuple.AddModificationTuple import AddModificationTuple
from xerial.modification.ModificationTuple.DropIndexModificationTuple import DropIndexModificationTuple
from xerial.modification.ModificationTuple.DropModificationTuple import DropModificationTuple
from xerial.modification.ModificationTuple.ModificationTuple import ModificationTuple
from xerial.modification.ModificationTuple.RenameModificationTuple import RenameModificationTuple
from xerial.modification.ModificationTuple.ChangeTypeModificationTuple import ChangeTypeModificationTuple
from xerial.modification.ModificationTuple.ChangeLengthModificationTuple import ChangeLengthModificationTuple


class ModificationTupleFactory:
    @staticmethod
    def create(
            table: str,
            version: str,
            modification_type: ModificationType,
            column_name: str,
            *args
    ) -> ModificationTuple:
        if modification_type == ModificationType.ADD:
            return AddModificationTuple(table, version, column_name, *args)
        elif modification_type == ModificationType.DROP:
            return DropModificationTuple(table, version, column_name, *args)
        elif modification_type == ModificationType.RENAME:
            return RenameModificationTuple(table, version, column_name, *args)
        elif modification_type == ModificationType.CHANGE_TYPE:
            return ChangeTypeModificationTuple(table, version, column_name, *args)
        elif modification_type == ModificationType.CHANGE_LENGTH:
            return ChangeLengthModificationTuple(table, version, column_name, *args)
        elif modification_type == ModificationType.ADD_INDEX:
            return AddIndexModificationTuple(table, version, column_name, *args)
        elif modification_type == ModificationType.DROP_INDEX:
            return DropIndexModificationTuple(table, version, column_name, *args)
        else:
            raise ValueError(f'Unknown modification type: {modification_type.name}')
