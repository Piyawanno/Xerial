from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Library(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    location = StringColumn()
