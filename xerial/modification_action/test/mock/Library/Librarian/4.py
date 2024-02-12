from xerial.DateColumn import DateColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.TimeColumn import TimeColumn


class Librarian(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    email = StringColumn()
    library = IntegerColumn(foreignKey="Library.id")
    phoneNumber = StringColumn(isFixedLength=True, length=10)
    address = StringColumn()
    DOB = DateColumn()
    startWorkingTime = TimeColumn()

    def modify(self):
        modification = self.createModification("1")
        modification.add("phoneNumber", StringColumn(isFixedLength=True, length=10))
        modification.add("address", StringColumn())

        modification = self.createModification("2")
        modification.add("DateOfBirth", DateColumn())

        modification = self.createModification("3")
        modification.rename(oldName="DateOfBirth", newName="DOB")

        modification = self.createModification("4")
        modification.add("startWorkingTime", TimeColumn())
