from typing import List

from xerial.Column import Column
from xerial.DateColumn import DateColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.Exception.DateTimeToDateException import DateTimeToDateException
from xerial.Exception.ModificationException import ModificationException
from xerial.Exception.TypeIncompatibleException import TypeIncompatibleException
from xerial.Modification.ModificationActon.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType


class ChangeTypeModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, oldColumn: Column, newColumn: Column) -> None:
        super().__init__(table, version, ModificationType.CHANGE_TYPE, name)
        self.oldColumn = oldColumn
        self.newColumn = newColumn

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.oldColumn.__class__.__name__}-{self.newColumn.__class__.__name__}'

    def tuple(self) -> tuple:
        return self.baseTuple(), self.oldColumn, self.newColumn

    def reverse_args(self) -> tuple:
        return self.columnName, self.oldColumn, self.newColumn

    def analyze(self) -> List[ModificationException]:
        exceptions: List[ModificationException] = []
        if self.newColumn not in self.oldColumn.compatible:
            exceptions.append(TypeIncompatibleException(
                self.columnName,
                self.oldColumn.__class__.__name__,
                self.newColumn.__name__
            ))

        if self.newColumn == DateColumn and self.oldColumn.__class__ == DateTimeColumn:
            exceptions.append(DateTimeToDateException(self.columnName))

        return exceptions
