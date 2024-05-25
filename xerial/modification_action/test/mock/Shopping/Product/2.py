from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Product(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    price = IntegerColumn()
    description = StringColumn(length=30)
    quantity = IntegerColumn()

    def modify(self):
        modification = self.createModification("1")
        modification.add("description", StringColumn(length=25))

        modification = self.createModification("2")
        modification.add("quantity", IntegerColumn())
        modification.changeLength("description", 30)
