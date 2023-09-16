from xerial.AsyncSQLiteDBSession import AsyncSQLiteDBSession
from xerial.AsyncPostgresDBSession import AsyncPostgresDBSession
from xerial.Vendor import Vendor
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.DateColumn import DateColumn
from xerial.Children import Children

from datetime import datetime
from typing import List

import asyncio, copy, time

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

	config = {
		"vendor" : Vendor.POSTGRESQL,
		"host" : "localhost",
		"database" : "Gaimon",
		"port": 5432,
		"user": "admin",
		"password": "SECRET_PASSWORD",
	}
	session = AsyncPostgresDBSession(config)
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

	pollList1 = [copy.copy(poll) for i in range(100)]
	pollList2 = [copy.copy(poll) for i in range(100)]

	await session.insert(poll)

	start = time.time()
	await session.insertMultiple(pollList1, True, True)
	print("Insert Multiple", time.time()- start)

	start = time.time()
	for poll in pollList2 :
		await session.insert(poll)
	print("Insert Each", time.time()- start)

	pollList:List[Poll] = await session.select(Poll, "ORDER BY id DESC", isRelated=True, hasChildren=True, limit=1)
	poll = pollList[0]

	poll.choices[-1].choice = "Sun is a star not a planet."
	poll.choices.append(Choice().fromDict({"choice" : "Pluto"}),)
	
	await session.update(poll)
	pollList:List[Poll] = await session.select(Poll, "ORDER BY id DESC", isRelated=True, limit=1)
	poll = pollList[0]
	pollID = poll.id

	await session.drop(poll)
	choiceList = await session.select(Choice, f"WHERE poll=?", parameter=[pollID])
	await session.closeConnection()
	return

asyncio.run(runTest())