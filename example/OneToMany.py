from xerial.SQLiteDBSession import SQLiteDBSession
from xerial.DBSessionBase import REGISTER
from xerial.Vendor import Vendor
from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.DateColumn import DateColumn
from xerial.Children import Children

from datetime import datetime
from typing import List
@REGISTER
class Poll (Record) :
	topic = StringColumn(length=64)
	description = StringColumn(length=-1)
	startDate = DateColumn()
	endDate = DateColumn()
	# Reference to Choice.poll
	choices = Children("Choice.poll")

	def __repr__(self) -> str:
		return f"{self.topic} {self.description} {self.startDate} {self.endDate} {self.choices}"

@REGISTER
class Choice (Record) :
	# Reference to Poll.id
	poll = IntegerColumn(foreignKey="Poll.id", isIndex=True)
	choice = StringColumn(length=128)
	count = IntegerColumn(default=0)

	def __repr__(self) -> str:
		return f"{self.id} {self.choice} {self.count}"

config = {
	"vendor" : Vendor.SQLITE,
	"database" : "./example.sqlite.bin"
}

session = SQLiteDBSession(config).init()

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

session.insert(poll)

pollList:List[Poll] = session.select(Poll, "ORDER BY id DESC", isRelated=True, hasChildren=True, limit=1)
poll = pollList[0]
print(poll)

poll.choices[-1].choice = "Sun is a star not a planet."
poll.choices.append(Choice().fromDict({"choice" : "Pluto"}),)
session.update(poll)
pollList:List[Poll] = session.select(Poll, "ORDER BY id DESC", isRelated=True, hasChildren=True, limit=1)
poll = pollList[0]
pollID = poll.id
print(poll)

session.drop(poll)
choiceList = session.select(Choice, f"WHERE poll=?", parameter=[pollID], hasChildren=True)
print(choiceList)