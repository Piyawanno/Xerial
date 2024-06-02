from xerial.DateTimeColumn import DateTimeColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record


class OrderItem(Record):
	id = IntegerColumn(isPrimary=True)
	date = DateTimeColumn()
	quantity = IntegerColumn()
	product = IntegerColumn(foreignKey="Product.id")
	shoppingOrder = IntegerColumn(foreignKey="ShoppingOrder.id")
