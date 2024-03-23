from typing import List

from xerial.Exception.ModificationException import ModificationException
from xerial.ModificationType import ModificationType


class ModificationAction:
    def __init__(self, table: str, version: str, modificationType: ModificationType, column_name: str) -> None:
        self.table = table
        self.version = version
        self.modificationType = modificationType
        self.columnName = column_name

    def prefix(self) -> str:
        return f'{self.table}-{self.version}-{self.modificationType.name}-{self.columnName}'

    def baseTuple(self) -> tuple:
        return self.modificationType, self.table, self.columnName

    def __str__(self) -> str:
        return self.prefix()

    def tuple(self) -> tuple:
        return self.baseTuple()

    def reverse_args(self) -> tuple:
        raise NotImplementedError('This method must be overridden in a subclass.')

    def analyze(self) -> List[ModificationException]:
        return []
