from xerial.Modification.ModificationActon.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class RenameModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, oldName: str, newName: str) -> None:
        super().__init__(table, version, ModificationType.RENAME, oldName)
        self.newName = newName

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.newName}'

    def tuple(self) -> tuple:
        return self.baseTuple(), self.newName

    def reverse_args(self) -> tuple:
        return self.columnName, self.newName
