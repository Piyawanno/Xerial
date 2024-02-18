from xerial.ModificationType import ModificationType
from xerial.modification.ModificationTuple.ModificationTuple import ModificationTuple


class DropIndexModificationTuple(ModificationTuple):
    def __init__(self, table: str, version: str, name: str) -> None:
        super().__init__(table, version, ModificationType.DROP_INDEX, name)

    def reverse_args(self) -> tuple:
        return self.column_name,
