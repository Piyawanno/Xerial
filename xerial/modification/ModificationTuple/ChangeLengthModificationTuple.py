from xerial.Column import Column
from xerial.ModificationType import ModificationType
from xerial.modification.ModificationTuple.ModificationTuple import ModificationTuple


class ChangeLengthModificationTuple(ModificationTuple):
    def __init__(self, table: str, version: str, name: str, column: Column) -> None:
        super().__init__(table, version, ModificationType.CHANGE_LENGTH, name)
        self.column = column
        self.length = column.length

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.length}'

    def tuple(self) -> tuple:
        return self.base_tuple(), self.column

    def reverse_args(self) -> tuple:
        return self.column_name, self.length
