from certifi import where
from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.Vendor import Vendor
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn

class Person (Record) :
	# For StringColumn recommended length < 255
	name = StringColumn(length=64)
	surname = StringColumn(length=64)
	# StringColumn with length == -1 : LongText data type.
	address = StringColumn(length=-1)
	age = IntegerColumn()

	# Column id is automatically generated.
	# If other primary key column is desired, column can be explicitly defined.
	def __repr__(self) -> str:
		return f"{self.id} {self.name} {self.surname} {self.age}"

"""
PostgreSQL

from xerial.PostgresDBSession import PostgresDBSession
config = {
	"vendor" : Vendor.POSTGRESQL,
	"host" : "localhost",
	"port" : 5432,
	"database" : "DB_NAME",
	"user" : "DB_USER_NAME",
	"password" : "DB_PASSWORD",
}

session = PostgresDBSession(config)
session.connect()
"""

"""
MariaDB/MySQL

from xerial.MariaDBSession import MariaDBSession
config = {
	"vendor" : Vendor.MARIADB,
	"host" : "localhost",
	"port" : 3306,
	"database" : "DB_NAME",
	"user" : "DB_USER_NAME",
	"password" : "DB_PASSWORD",
}

session = MariaDBSession(config)
session.connect()
"""

"""
Oracle

from xerial.OracleDBSession import OracleDBSession
config = {
	"vendor" : Vendor.ORACLE,
	"host" : "localhost",
	"port" : 1521,
	"database" : "DB_NAME",
	"user" : "DB_USER_NAME",
	"password" : "DB_PASSWORD",
	"domain" : "XEPDB1",
	"owner" : ["DB_OWNER"],
}

session = OracleDBSession(config)
session.connect()
"""

"""
MS SQL Server

Default User : SA

Full documentation

https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash

Installation of MS SQL Server Driver for ODBC

https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15


from xerial.MSSQLDBSession import MSSQLDBSession
config = {
	"vendor" : Vendor.ORACLE,
	"host" : "localhost",
	"port" : 1433,
	"database" : "DB_NAME",
	"user" : "SA",
	"password" : "DB_PASSWORD",
	"driver" : "ODBC Driver 18 for SQL Server",
}

session = MSSQLDBSession(config)
session.connect()
"""

config = {
	"vendor" : Vendor.SQLITE,
	"database" : "./example.sqlite.bin"
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

import random, string
charSet = string.ascii_letters + string.digits

personList = []
for i in range(1_000) :
	person = Person()
	person.name = ''.join([random.choice(charSet) for i in range(16)])
	person.surname = ''.join([random.choice(charSet) for i in range(16)])
	person.address = ''.join([random.choice(charSet) for i in range(512)])
	person.age = random.randint(20, 80)
	personList.append(person)

session.insertMultiple(personList)

# WHERE, ORDER BY, ORDER BY DESC, GROUP BY clause can be directly apply to select.
paginated = session.select(Person, "WHERE age > 30 ORDER BY age", limit=20, offset=60)
for person in paginated :
	print(person)