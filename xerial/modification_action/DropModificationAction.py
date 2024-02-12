from xerial.Column import Column
from xerial.modification_action.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class DropModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, column: Column) -> None:
        super().__init__(table, version, ModificationType.DROP, name, column)
        self.column = column

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.column.__class__.__name__}'

    def reverseArgs(self) -> tuple:
        return self.columnName, self.column

    def verbose(self) -> str:
        return f'Drop {self.column.__class__.__name__} {self.columnName} from {self.table}'
