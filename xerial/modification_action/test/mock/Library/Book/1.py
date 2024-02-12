from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Book(Record):
    id = StringColumn(isPrimary=True, isFixedLength=True, length=13)
    bookTitle = StringColumn()
    author = StringColumn()
    publishedYear = StringColumn(isFixedLength=True, length=4)
    library = IntegerColumn(foreignKey="Library.id")

    def modify(self):
        modification = self.createModification("1")
        modification.rename(oldName="title", newName="bookTitle")
