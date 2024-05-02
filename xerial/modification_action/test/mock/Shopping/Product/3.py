from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Product(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    price = IntegerColumn()
    quantity = IntegerColumn()

    def modify(self):
        modification = self.createModification("1")
        modification.add("description", StringColumn(isFixedLength=True, length=25))

        modification = self.createModification("2")
        modification.add("quantity", IntegerColumn())
        modification.changeLength("description", 30)

        modification = self.createModification("3")
        modification.drop("description", StringColumn(isFixedLength=True, length=30))
