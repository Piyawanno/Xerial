from xerial.Record import Record
from xerial.column.StringColumn import StringColumn

class WorkerStructure (Record) :
	division = StringColumn(length=64)
	section = StringColumn(length=64)
	line = StringColumn(length=64)