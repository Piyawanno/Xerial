from xerial.DateColumn import DateColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Library(Record):
    id = IntegerColumn(isPrimary=True)
    libraryName = StringColumn()
    location = StringColumn()
    createDate = DateColumn()
    telephone = StringColumn(isFixedLength=True, length=10)

    def modify(self):
        modification = self.createModification("1")
        modification.rename(oldName="name", newName="libraryName")

        modification = self.createModification("2")
        modification.add("createDate", DateColumn())

        modification = self.createModification("3")
        modification.add("telephone", StringColumn(isFixedLength=True, length=10))
