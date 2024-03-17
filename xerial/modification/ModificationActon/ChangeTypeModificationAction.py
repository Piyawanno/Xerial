from typing import List

from xerial.Column import Column
from xerial.DateColumn import DateColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.ModificationType import ModificationType
from xerial.exception.DateTimeToDateException import DateTimeToDateException
from xerial.exception.ModificationException import ModificationException
from xerial.exception.TypeIncompatibleException import TypeIncompatibleException
from xerial.modification.ModificationActon.ModificationAction import ModificationAction


class ChangeTypeModificationAction(ModificationAction):
    def __init__(self, table: str, version: str, name: str, old_column: Column, new_column: Column) -> None:
        super().__init__(table, version, ModificationType.CHANGE_TYPE, name)
        self.old_column = old_column
        self.new_column = new_column

    def __str__(self) -> str:
        return f'{self.prefix()}-{self.old_column.__class__.__name__}-{self.new_column.__class__.__name__}'

    def tuple(self) -> tuple:
        return self.base_tuple(), self.old_column, self.new_column

    def reverse_args(self) -> tuple:
        return self.column_name, self.old_column, self.new_column

    def analyze(self) -> List[ModificationException]:
        exceptions: List[ModificationException] = []
        if self.new_column not in self.old_column.compatible:
            exceptions.append(TypeIncompatibleException(
                self.column_name,
                self.old_column.__class__.__name__,
                self.new_column.__name__
            ))

        if self.new_column == DateColumn and self.old_column.__class__ == DateTimeColumn:
            exceptions.append(DateTimeToDateException(self.column_name))

        return exceptions
