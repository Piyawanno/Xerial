from xerial.ModificationType import ModificationType
from xerial.modification.ModificationTuple.ModificationTuple import ModificationTuple


class RenameModificationTuple(ModificationTuple):
    def __init__(self, table: str, version: str, old_name: str, new_name: str) -> None:
        super().__init__(table, version, ModificationType.RENAME, old_name)
        self.new_name = new_name

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.new_name}'

    def tuple(self) -> tuple:
        return self.base_tuple(), self.new_name

    def reverse_args(self) -> tuple:
        return self.column_name, self.new_name
