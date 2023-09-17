# Many-to-Many Relation

Many-to-Many relation is not a trivial task in the database design.
Xerial uses the **mapper** pattern for the implementation. The mapper
is an extra Model/table, which links between 2 Models/tables.

```python
from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Children import Children
from enum import IntEnum


class WarehouseType (IntEnum) :
	SUPPLIER = 1
	PRODUCTION = 2
	CUSTOMER = 3

class ProductType (Record) :
	name = StringColumn(length=32, isRepresentative=True)
	description = StringColumn(length=-1)
	warehouse = Children("ProductWareHouseMapper.productTypeID")

	def __repr__(self) -> str:
		return f"<ProductType {self.id}, {self.name}, {self.description}, {self.warehouse}>"

class WareHouse (Record) :
	name = StringColumn(length=32, isRepresentative=True)
	location = StringColumn(length=255)
	type = IntegerColumn(enum=WarehouseType)
	productType = Children("ProductWareHouseMapper.warehouseID")

	def __repr__(self) -> str:
		return f"<WareHouse {self.id}, {self.name} {self.location}, {self.productType}>"

class ProductWareHouseMapper (Record) :
	__is_mapper__ = True
	productTypeID = IntegerColumn(foreignKey="ProductType.id")
	warehouseID = IntegerColumn(foreignKey="WareHouse.id")

	def __repr__(self) -> str:
		return f"<ProductWareHouseMapper {self.id} P={self.productTypeID} W={self.warehouseID}>"

session = SQLiteDBSession(config)
session.connect()
session.appendModel(ProductType)
session.appendModel(WareHouse)
session.appendModel(ProductWareHouseMapper)
session.checkModelLinking()
session.createTable()
```

From the example, `ProductWareHouseMapper` is the mapper Model, which links
between the `ProductType` and the `WareHouse`. Note that the relations
of these 3 Models are bidirectional. `WareHouse`
will link to the `ProductWareHouseMapper` over 
`productType = Children("ProductWareHouseMapper.warehouseID")` and vice versa
over `warehouseID = IntegerColumn(foreignKey="WareHouse.id")`.
The other relation from `ProductType` to `ProductWareHouseMapper`
will be created over `warehouse = Children("ProductWareHouseMapper.productTypeID")`
and `productTypeID = IntegerColumn(foreignKey="ProductType.id")`.
Note that the Mapper Model `ProductWareHouseMapper` must set the class attribute
`__is_mapper__ = True` so that Xerial will remark the relation.

Data can be inserted as shown in the followed code:

```python
warehouseList = [
	WareHouse().fromDict({"name" : "WH1", "location" : "Konohakagure", "type" : 1}),
	WareHouse().fromDict({"name" : "WH2", "location" : "Kumogakure", "type" : 2}),
	WareHouse().fromDict({"name" : "WH3", "location" : "Iwagakure", "type" : 3}),
]

session.insertMultiple(warehouseList)

summonSeal = ProductType()
summonSeal.name = "Summon Seal"
summonSeal.description = "You can pack anything in it and summon them back any time you want."
summonSeal.warehouse = [
	ProductWareHouseMapper().fromDict({"warehouseID" : warehouseList[0].toDict()}),
	ProductWareHouseMapper().fromDict({"warehouseID" : warehouseList[1].toDict()})
]

session.insert(summonSeal)

shuriken = ProductType()
shuriken.name = "Shuriken"
shuriken.description = "A concealed weapon that was used as a hidden dagger or metsubushi to distract or misdirect."
shuriken.warehouse = [
	ProductWareHouseMapper().fromDict({"warehouseID" : warehouseList[0].toDict()}),
	ProductWareHouseMapper().fromDict({"warehouseID" : warehouseList[2].toDict()})
]

session.insert(shuriken)
```

Note that data can be inserted or updated from each side of data. In our case,
records of `WareHouse` can be firstly inserted or `ProductType` first.
The condition is that by data ingest, data of only 2 layers are ingested.
From the example, `session.insert(summonSeal)` will insert `ProductType`
and then `ProductWareHouseMapper` and not further. Hence, data of one side
(`WareHouse`) must be inserted followed by the other side (`ProductType`).
The mapper data will automatically ingested. The sequence has no effect.

The following code show, how data can be selected :

```python
fetchedWarehouse = session.select(WareHouse, "", isRelated=True, hasChildren=True)

import json
print(json.dumps([i.toDict() for i in fetchedWarehouse], indent=4))
```

From the given code, the result will be:
```json
[
    {
        "productType": [
            {
                "productTypeID": {
                    "warehouse": [],
                    "id": 1,
                    "description": "You can pack anything in it and summon them back any time you want.",
                    "name": "Summon Seal"
                },
                "id": 1,
                "warehouseID": 1
            },
            {
                "productTypeID": {
                    "warehouse": [],
                    "id": 2,
                    "description": "A concealed weapon that was used as a hidden dagger or metsubushi to distract or misdirect.",
                    "name": "Shuriken"
                },
                "id": 3,
                "warehouseID": 1
            }
        ],
        "id": 1,
        "location": "Konohakagure",
        "name": "WH1",
        "type": 1
    },
    {
        "productType": [
            {
                "productTypeID": {
                    "warehouse": [],
                    "id": 1,
                    "description": "You can pack anything in it and summon them back any time you want.",
                    "name": "Summon Seal"
                },
                "id": 2,
                "warehouseID": 2
            }
        ],
        "id": 2,
        "location": "Kumogakure",
        "name": "WH2",
        "type": 2
    },
    {
        "productType": [
            {
                "productTypeID": {
                    "warehouse": [],
                    "id": 2,
                    "description": "A concealed weapon that was used as a hidden dagger or metsubushi to distract or misdirect.",
                    "name": "Shuriken"
                },
                "id": 4,
                "warehouseID": 3
            }
        ],
        "id": 3,
        "location": "Iwagakure",
        "name": "WH3",
        "type": 3
    }
]
```