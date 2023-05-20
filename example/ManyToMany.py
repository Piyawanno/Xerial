from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.Vendor import Vendor
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


config = {
	"vendor" : Vendor.SQLITE,
	"database" : "./example.sqlite.bin"
}

session = SQLiteDBSession(config)
session.connect()
session.appendModel(ProductType)
session.appendModel(WareHouse)
session.appendModel(ProductWareHouseMapper)
session.checkModelLinking()
session.createTable()

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

shuriken = ProductType()
shuriken.name = "Shuriken"
shuriken.description = "A concealed weapon that was used as a hidden dagger or metsubushi to distract or misdirect."
shuriken.warehouse = [
	ProductWareHouseMapper().fromDict({"warehouseID" : warehouseList[0].toDict()}),
	ProductWareHouseMapper().fromDict({"warehouseID" : warehouseList[2].toDict()})
]

session.insert(summonSeal)
session.insert(shuriken)

session.selectExcel("ProductWareHouseMapper.xlsx", ProductWareHouseMapper, "")

fetchedWarehouse = session.select(WareHouse, "", isRelated=True)
for i in fetchedWarehouse :
	print(f"Warehouse {i.name}")
	for j in i.productType :
		print(j)

print([i.toDict() for i in fetchedWarehouse])

fetchedProduct = session.select(ProductType, "", isRelated=True)
for i in fetchedProduct :
	print(f"Product {i.name} {i.toOption()}")
	for j in i.warehouse :
		print(j)
print([i.toDict() for i in fetchedProduct])

session.drop(fetchedProduct[0])
print("AFTER DROP ProductType")

fetchedWarehouse = session.select(WareHouse, "", isRelated=True)
for i in fetchedWarehouse :
	print(f"Warehouse {i.name}")
	for j in i.productType :
		print(j)
print([i.toDict() for i in fetchedWarehouse])


