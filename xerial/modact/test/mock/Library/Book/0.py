from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Book(Record):
	id = StringColumn(isPrimary=True, isFixedLength=True, length=13)
	title = StringColumn()
	author = StringColumn()
	publishedYear = StringColumn(isFixedLength=True, length=4)
	library = IntegerColumn(foreignKey="Library.id")
