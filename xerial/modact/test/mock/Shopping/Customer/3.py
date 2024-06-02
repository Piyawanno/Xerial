from xerial.FractionColumn import FractionColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Customer(Record):
	id = IntegerColumn(isPrimary=True)
	name = StringColumn()
	email = StringColumn()
	phoneNumber = StringColumn(isFixedLength=True, length=10)

	def modify(self):
		modification = self.createModification("1")
		modification.add("salary", FractionColumn())
		modification.add("totalProductBought", FractionColumn())

		modification = self.createModification("2")
		modification.add("phoneNumber", StringColumn(isFixedLength=True, length=10))
		modification.drop("totalProductBought", FractionColumn())

		modification = self.createModification("3")
		modification.drop("salary", FractionColumn())
