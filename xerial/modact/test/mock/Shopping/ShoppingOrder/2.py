from xerial.DateTimeColumn import DateTimeColumn
from xerial.FloatColumn import FloatColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record


class ShoppingOrder(Record):
	id = IntegerColumn(isPrimary=True)
	date = DateTimeColumn()
	customer = IntegerColumn(foreignKey="Customer.id")
	discountRate = FloatColumn(precision=2)
	totalPrice = IntegerColumn()

	def modify(self):
		modification = self.createModification("1")
		modification.add("discount", FloatColumn(precision=2))
		modification.add("totalPrice", IntegerColumn())

		modification = self.createModification("2")
		modification.rename(oldName="discount", newName="discountRate")
