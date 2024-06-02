from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Librarian(Record):
	id = IntegerColumn(isPrimary=True)
	name = StringColumn()
	email = StringColumn()
	library = IntegerColumn(foreignKey="Library.id")
	phoneNumber = StringColumn(isFixedLength=True, length=10)
	address = StringColumn()

	def modify(self):
		modification = self.createModification("1")
		modification.add("phoneNumber", StringColumn(isFixedLength=True, length=10))
		modification.add("address", StringColumn())
