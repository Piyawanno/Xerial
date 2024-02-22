from xerial.ModificationType import ModificationType
from xerial.exception.ModificationException import ModificationException


class ModificationAction:
    def __init__(self, table: str, version: str, modification_type: ModificationType, column_name: str) -> None:
        self.table = table
        self.version = version
        self.modification_type = modification_type
        self.column_name = column_name

    def prefix(self) -> str:
        return f'{self.table}-{self.version}-{self.modification_type.name}-{self.column_name}'

    def base_tuple(self) -> tuple:
        return self.modification_type, self.table, self.column_name

    def __str__(self) -> str:
        return self.prefix()

    def tuple(self) -> tuple:
        return self.base_tuple()

    def reverse_args(self) -> tuple:
        raise NotImplementedError('This method must be overridden in a subclass.')

    def analyze(self) -> ModificationException or None:
        return None
