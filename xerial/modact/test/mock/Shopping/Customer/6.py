from xerial.Children import Children
from xerial.FractionColumn import FractionColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Customer(Record):
	id = IntegerColumn(isPrimary=True)
	name = StringColumn()
	email = StringColumn()
	salary = FractionColumn()

	def modify(self):
		modification = self.createModification("1")
		modification.add("salary", FractionColumn())
		modification.add("totalProductBought", FractionColumn())

		modification = self.createModification("2")
		modification.add("phoneNumber", StringColumn(isFixedLength=True, length=10))
		checkout6To1 = modification.drop("totalProductBought", FractionColumn())

		modification = self.createModification("3")
		modification.drop("salary", FractionColumn())

		modification = self.createModification("4")
		modification.add("address", StringColumn())

		self.createCheckout(modificationVersion="5", destination="2")

		self.createCheckout(modificationVersion="6", destination="1", skip=[checkout6To1])
