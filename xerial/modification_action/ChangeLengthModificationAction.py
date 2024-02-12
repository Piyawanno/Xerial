from xerial.Column import Column
from xerial.modification_action.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class ChangeLengthModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, column: Column) -> None:
        super().__init__(table, version, ModificationType.CHANGE_LENGTH, name, column)
        self.column = column
        self.length = column.length

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.length}'

    def tuple(self) -> tuple:
        return self.baseTuple() + (self.column,)

    def reverseArgs(self) -> tuple:
        return self.columnName, self.length

    def verbose(self) -> str:
        return f'Change {self.column.__class__.__name__} {self.columnName} length to {self.length} in {self.table}'
