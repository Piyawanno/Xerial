from xerial.DateColumn import DateColumn
from xerial.FloatColumn import FloatColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Student(Record):
    # id = IntegerColumn(isPrimary=True)  # modification3-rename
    studentID = IntegerColumn(isPrimary=True)
    firstName = StringColumn(length=150)
    lastName = StringColumn(length=150)
    joined = DateColumn()
    # age = IntegerColumn()  # modification2-drop
    # gpax = IntegerColumn()  # modification2-changeType old
    gpax = FloatColumn()  # modification2-changeType new

    def modify(self):
        modification = self.createModification("1")
        modification.changeLength("firstName", 150)
        modification.changeLength("lastName", 150)

        modification = self.createModification("2")
        exampleSkipKey = modification.changeType(
            name="gpax",
            oldColumn=IntegerColumn(),
            newColumn=FloatColumn()
        )  # changeType need OLD Column and NEW Column now
        modification.drop("age", IntegerColumn())  # drop need Column object now

        modification = self.createModification("3")
        modification.rename("id", "studentID")

        self.createCheckout(
            modificationVersion="4",
            destination="1",
            skip=[exampleSkipKey],
        )
