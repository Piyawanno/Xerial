from xerial.Column import Column
from xerial.ModificationType import ModificationType
from xerial.modification.ModificationTuple.ModificationTuple import ModificationTuple


class ChangeTypeModificationTuple(ModificationTuple):
    def __init__(self, table: str, version: str, name: str, old_column: Column, new_column: Column) -> None:
        super().__init__(table, version, ModificationType.CHANGE_TYPE, name)
        self.old_column = old_column
        self.new_column = new_column

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.old_column.__class__.__name__}-{self.new_column.__class__.__name__}'

    def tuple(self) -> tuple:
        return self.base_tuple(), self.old_column, self.new_column

    def reverse_args(self) -> tuple:
        return self.column_name, self.old_column, self.new_column
