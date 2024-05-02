from xerial.Children import Children
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Customer(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    email = StringColumn()
