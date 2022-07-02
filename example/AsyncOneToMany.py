from xerial.AsyncSQLiteDBSession import AsyncSQLiteDBSession
from xerial.Vendor import Vendor
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.DateColumn import DateColumn
from xerial.Children import Children

from datetime import datetime
from typing import List

import asyncio

class Poll (Record) :
	topic = StringColumn(length=64)
	description = StringColumn(length=-1)
	startDate = DateColumn()
	endDate = DateColumn()
	# Reference to Choice.poll
	choices = Children("Choice.poll")

	def __repr__(self) -> str:
		return f"{self.topic} {self.description} {self.startDate} {self.endDate} {self.choices}"

class Choice (Record) :
	# Reference to Poll.id
	poll = IntegerColumn(foreignKey="Poll.id", isIndex=True)
	choice = StringColumn(length=128)
	count = IntegerColumn(default=0)

	def __repr__(self) -> str:
		return f"{self.id} {self.choice} {self.count}"

async def runTest() :
	# config = {
	# 	"vendor" : Vendor.SQLITE,
	# 	"database" : "./example.sqlite.bin"
	# }

	# session = AsyncSQLiteDBSession(config)
	
	from xerial.AsyncOracleDBSession import AsyncOracleDBSession
	config = {
		"vendor" : Vendor.ORACLE,
		"host" : "localhost",
		"port" : 1521,
		"database" : "RedShip",
		"user" : "admin",
		"password" : "NotSecret#2475",
		"domain" : "XEPDB1",
		"owner" : ["ADMIN"],
	}


	session = AsyncOracleDBSession(config)
	await session.connect()

	session.appendModel(Poll)
	session.appendModel(Choice)
	await session.createTable()

	poll = Poll()
	poll.topic = "On which planet do you want to live?"
	poll.description = "In the case of russian invasion on the whole planet earth, "
	"because Putin said, everyone on earth is fascism excepted Putin's supporter."
	poll.startDate = datetime.strptime("2022-02-24", "%Y-%m-%d")
	poll.endDate = datetime.strptime("2029-01-01", "%Y-%m-%d")
	poll.choices = [
		Choice().fromDict({"choice" : "Mars"}),
		Choice().fromDict({"choice" : "Jupiter"}),
		Choice().fromDict({"choice" : "Moon"}),
		Choice().fromDict({"choice" : "Sun"}),
	]

	await session.insert(poll)

	pollList:List[Poll] = await session.select(Poll, "ORDER BY id DESC", isRelated=True, limit=1)
	poll = pollList[0]
	print(poll)

	poll.choices[-1].choice = "Sun is a star not a planet."
	await session.update(poll)
	pollList:List[Poll] = await session.select(Poll, "ORDER BY id DESC", isRelated=True, limit=1)
	poll = pollList[0]
	pollID = poll.id
	print(poll)

	await session.drop(poll)
	choiceList = await session.select(Choice, f"WHERE poll={pollID}")
	print(choiceList)
	await session.closeConnection()
	return

asyncio.run(runTest())