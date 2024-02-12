from xerial.DateTimeColumn import DateTimeColumn
from xerial.FloatColumn import FloatColumn
from xerial.FractionColumn import FractionColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record


class OrderItem(Record):
    id = IntegerColumn(isPrimary=True)
    date = DateTimeColumn()
    quantity = IntegerColumn()
    product = IntegerColumn(foreignKey="Product.id")
    shoppingOrder = IntegerColumn(foreignKey="ShoppingOrder.id")
    totalPrice = FractionColumn()

    def modify(self):
        modification = self.createModification("1")
        modification.add("totalPrice", FloatColumn())

        modification = self.createModification("2")
        modification.changeType("totalPrice", oldColumn=FloatColumn(), newColumn=FractionColumn())