from re import I
from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.Vendor import Vendor
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn

class Person (Record) :
	name = StringColumn(length=64)
	surname = StringColumn(length=64)
	address = StringColumn(length=-1)
	age = IntegerColumn()


config = {
	"vendor" : Vendor.SQLITE,
	"database" : "./person.sqlite.bin"
}

session = SQLiteDBSession(config)
session.connect()
session.appendModel(Person)
session.createTable()

person = Person().fromDict({
	"name" : "Kittipong",
	"surname" : "Piyawanno",
	"address" : "Earth",
	"age" : 10_000
})

session.insert(person)
personList = session.select(Person, "")
print([i.toDict() for i in personList])

person = personList[0]
person.age = 20_000
session.update(person)

personList = session.select(Person, "")
print([i.toDict() for i in personList])

person = personList[0]
session.drop(person)
