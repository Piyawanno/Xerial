from xerial.Modification.ModificationActon.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class DropIndexModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str) -> None:
        super().__init__(table, version, ModificationType.DROP_INDEX, name)

    def reverse_args(self) -> tuple:
        return self.columnName,
