from typing import List

from xerial.Column import Column
from xerial.DateColumn import DateColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.exception.DateTimeToDateException import DateTimeToDateException
from xerial.exception.ModificationException import ModificationException
from xerial.exception.TypeIncompatibleException import TypeIncompatibleException
from xerial.FloatColumn import FloatColumn
from xerial.FractionColumn import FractionColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.JSONColumn import JSONColumn
from xerial.modification_action.ModificationAction import ModificationAction
from xerial.ModificationType import ModificationType
from xerial.StringColumn import StringColumn


class ChangeTypeModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, oldColumn: Column, newColumn: Column) -> None:
        super().__init__(table, version, ModificationType.CHANGE_TYPE, name, oldColumn)
        self.oldColumn = oldColumn
        self.newColumn = newColumn
        self.compatibles = {
            StringColumn: {JSONColumn},
            JSONColumn: {StringColumn},
            DateColumn: {DateTimeColumn},
            DateTimeColumn: {DateColumn},
            IntegerColumn: {FloatColumn, FractionColumn},
            FloatColumn: {IntegerColumn, FractionColumn},
        }

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.oldColumn.__class__.__name__}-{self.newColumn.__class__.__name__}'

    def tuple(self) -> tuple:
        return self.baseTuple() + (self.newColumn,)

    def reverseArgs(self) -> tuple:
        return self.columnName, self.oldColumn, self.newColumn

    def verbose(self) -> str:
        return (f'Change data type of {self.columnName} '
                f'from {self.oldColumn.__class__.__name__} '
                f'to {self.newColumn.__class__.__name__} '
                f'in {self.table}')

    def analyze(self) -> List[ModificationException]:
        exceptions: List[ModificationException] = []
        if self.newColumn.__class__ not in self.compatibles.get(self.oldColumn.__class__, set()):
            exceptions.append(TypeIncompatibleException(
                self.columnName,
                self.oldColumn.__class__.__name__,
                self.newColumn.__class__.__name__
            ))

        if self.newColumn == DateColumn and self.oldColumn.__class__ == DateTimeColumn:
            exceptions.append(DateTimeToDateException(self.columnName))

        return exceptions
