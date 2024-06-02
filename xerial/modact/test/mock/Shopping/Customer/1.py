from xerial.FractionColumn import FractionColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Customer(Record):
	id = IntegerColumn(isPrimary=True)
	name = StringColumn()
	email = StringColumn()
	salary = FractionColumn()
	totalProductBought = FractionColumn()

	def modify(self):
		modification = self.createModification("1")
		modification.add("salary", FractionColumn())
		modification.add("totalProductBought", FractionColumn())
