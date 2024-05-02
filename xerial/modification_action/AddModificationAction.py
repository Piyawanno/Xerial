from xerial.Column import Column
from xerial.modification_action.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class AddModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, column: Column) -> None:
        super().__init__(table, version, ModificationType.ADD, name, column)

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.column.__class__.__name__}'

    def tuple(self) -> tuple:
        return self.baseTuple() + (self.column,)

    def reverseArgs(self) -> tuple:
        return self.columnName, self.column

    def verbose(self) -> str:
        return f'Add {self.column.__class__.__name__} {self.columnName} to {self.table}'
