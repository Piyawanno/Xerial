from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Librarian(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    email = StringColumn()
    library = IntegerColumn(foreignKey="Library.id")
