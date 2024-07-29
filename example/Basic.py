from xerial.DBSessionBase import REGISTER
from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.Vendor import Vendor
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.FractionColumn import FractionColumn
from xerial.CurrencyColumn import CurrencyColumn
from xerial.CurrencyData import CurrencyData
from fractions import Fraction
from enum import IntEnum
from datetime import datetime

import io, time

@REGISTER
class Gender (IntEnum) :
	MALE = 1
	FEMALE = 2

@REGISTER
class Person (Record) :
	# For StringColumn recommended length < 255
	name = StringColumn(length=64)
	surname = StringColumn(length=64)
	gender = IntegerColumn(enum=Gender)
	# StringColumn with length == -1 : LongText data type.
	address = StringColumn(length=-1)
	age = IntegerColumn()
	salary = FractionColumn()
	expense = CurrencyColumn()
	lastAttendance = DateTimeColumn(default=datetime.now)

	# Column id is automatically generated.
	# If other primary key column is desired, column can be explicitly defined.
	def __repr__(self) -> str:
		return f"{self.id} {self.name} {self.surname} {self.age} {self.salary} {self.expense}"

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

session = SQLiteDBSession(config).init()

person = Person().fromDict({
	"name" : "Kittipong",
	"surname" : "Piyawanno",
	"address" : "Earth",
	"age" : 10_000,
	"gender" : 1,
	"salary" : "32000.33",
	"expense" : CurrencyData("12000.33").toDict()
})

print(person.lastAttendance, type(person.lastAttendance))

session.insert(person)
personList = session.select(Person, "WHERE name LIKE ?", parameter=["Kit%"])
print([i.name for i in personList])

person = personList[0]
person.age = 20_000
session.update(person)

personList = session.select(Person, "")
# print([i.toDict() for i in personList])

with open("Person.csv", "wt") as fd :
	session.selectCSV(fd, Person, "")

session.selectExcel("Person.xlsx", Person, "")

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
	person.gender = i%2 + 1
	person.age = random.randint(20, 80)
	person.salary = Fraction(random.randint(2_000_000, 6_000_000), 100)
	person.expense = CurrencyData("10000/7")
	personList.append(person)

start = time.time()
session.insertMultiple(personList)
print(f">>> Total insert {time.time()-start}s")

# WHERE, ORDER BY, ORDER BY DESC, GROUP BY clause can be directly apply to select.
start = time.time()
paginated = session.select(Person, "WHERE age > 30 ORDER BY age", limit=20, offset=60)
print(f">>> Total select {time.time()-start}s")
for person in paginated :
	print(person)