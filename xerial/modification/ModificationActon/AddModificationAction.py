from xerial.Column import Column
from xerial.ModificationType import ModificationType
from xerial.modification.ModificationActon.ModificationAction import ModificationAction


class AddModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, column: Column) -> None:
        super().__init__(table, version, ModificationType.ADD, name)
        self.column = column

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.column.__class__.__name__}'

    def tuple(self) -> tuple:
        return self.base_tuple(), self.column

    def reverse_args(self) -> tuple:
        return self.column_name, self.column
