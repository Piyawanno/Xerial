from xerial.DateColumn import DateColumn
from xerial.FloatColumn import FloatColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.ModificationType import ModificationType
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Student(Record):
    studentID = IntegerColumn(isPrimary=True, isAutoIncrement=True)
    firstName = StringColumn(length=150)
    lastName = StringColumn(length=150)
    joined = DateColumn()
    gpax = FloatColumn()

    def modify(self):
        modification = self.createModification("1")
        modification.changeLength("firstName", 150)
        modification.changeLength("lastName", 150)

        modification = self.createModification("2")
        modification.changeType(
            name="gpax",
            oldColumn=IntegerColumn(),
            newColumn=FloatColumn()
        )  # changeType need OLD Column and NEW Column now
        modification.drop("age", IntegerColumn())  # drop need Column object now
        modification = self.createModification("3")
        modification.rename("id", "studentID")

        self.createCheckout(
            destination="1",
            skip={
                "2": [
                    (ModificationType.CHANGE_TYPE, self.__full_table_name__, "gpax", IntegerColumn(), FloatColumn()),
                    # Need optimization/refactor for this
                ],
            }
        )
