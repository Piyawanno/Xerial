from xerial.DateColumn import DateColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.Record import Record
from xerial.StringColumn import StringColumn


class Library(Record):
	id = IntegerColumn(isPrimary=True)
	libraryName = StringColumn()
	location = StringColumn()
	createDate = DateColumn()

	def modify(self):
		modification = self.createModification("1")
		modification.rename(oldName="name", newName="libraryName")

		modification = self.createModification("2")
		modification.add("createDate", DateColumn())
