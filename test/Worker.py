from xerial.Record import Record
from xerial.column.IntegerColumn import IntegerColumn
from xerial.column.FloatColumn import FloatColumn
from xerial.column.StringColumn import StringColumn

class Worker (Record) :
	workerID = IntegerColumn(isPrimary=True)
	structure = IntegerColumn(foreignKey='WorkerStructure.id')
	workerNo = StringColumn(length=20)
	firstName = StringColumn(length=200)
	lastName = StringColumn(length=200)
	departmentID = IntegerColumn()
	companyID = IntegerColumn(length=32)
	salary = FloatColumn(length=32, precision=10)
