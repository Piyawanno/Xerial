from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Product(Record):
	id = IntegerColumn(isPrimary=True)
	name = StringColumn()
	price = IntegerColumn()
