from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Product(Record):
    id = IntegerColumn(isPrimary=True)
    name = StringColumn()
    price = price = IntegerColumn()
    description = StringColumn(length=25)

    def modify(self):
        modification = self.createModification("1")
        modification.add("description", StringColumn(length=25))
