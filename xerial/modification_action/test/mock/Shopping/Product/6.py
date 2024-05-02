from xerial.FloatColumn import FloatColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Product(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    price = IntegerColumn()
    description = StringColumn(isFixedLength=True, length=30)

    def modify(self):
        modification = self.createModification("1")
        modification.add("description", StringColumn(isFixedLength=True, length=25))

        modification = self.createModification("2")
        modification.add("quantity", IntegerColumn())
        modification.changeLength("description", 30)

        modification = self.createModification("3")
        modification.drop("description", StringColumn(isFixedLength=True, length=30))

        modification = self.createModification("4")
        modification.add("discountRate", FloatColumn(precision=2))
        modification.changeType("price", oldColumn=IntegerColumn(), newColumn=FloatColumn(precision=2))

        self.createCheckout(modificationVersion="5", destination="2")

        self.createCheckout(modificationVersion="6", destination="1")
