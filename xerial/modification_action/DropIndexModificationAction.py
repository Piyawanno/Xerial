from xerial.Column import Column
from xerial.modification_action.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class DropIndexModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, column: Column) -> None:
        super().__init__(table, version, ModificationType.DROP_INDEX, name, column)

    def reverseArgs(self) -> tuple:
        return self.columnName,

    def verbose(self) -> str:
        return f'Drop index {self.columnName} from {self.table}'
