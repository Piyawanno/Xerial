from xerial.DateTimeColumn import DateTimeColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record


class ShoppingOrder(Record):
	id = IntegerColumn(isPrimary=True)
	date = DateTimeColumn()
	customer = IntegerColumn(foreignKey="Customer.id")
