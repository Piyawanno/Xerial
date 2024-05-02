from xerial.DateColumn import DateColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Library(Record):
    id = IntegerColumn(isPrimary=True)
    libraryName = StringColumn()
    location = StringColumn()
    telephone = StringColumn(isFixedLength=True, length=10)

    def modify(self):
        modification = self.createModification("1")
        modification.rename(oldName="name", newName="libraryName")

        modification = self.createModification("2")
        modification.add("createDate", DateColumn())

        modification = self.createModification("3")
        checkout4To1 = modification.add("telephone", StringColumn(isFixedLength=True, length=10))

        self.createCheckout(modificationVersion="4", destination="1", skip=[checkout4To1])
