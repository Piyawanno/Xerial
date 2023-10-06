from enum import IntEnum
from xerial.column.IntegerColumn import IntegerColumn
from xerial.column.FloatColumn import FloatColumn
from xerial.column.StringColumn import StringColumn
from xerial.column.DateColumn import DateColumn
from xerial.column.DateTimeColumn import DateTimeColumn
from xerial.column.TimeColumn import TimeColumn
from xerial.column.DayIntervalColumn import DayIntervalColumn
from xerial.column.JSONColumn import JSONColumn

class ColumnType (IntEnum) :
	INTEGER = 11
	FLOAT = 12
	STRING = 21
	DATE = 31
	DATE_TIME = 32
	TIME = 33
	DAY_INTERVAL = 34
	JSON = 40

ColumnType.mapped = {
	ColumnType.INTEGER:IntegerColumn,
	ColumnType.FLOAT:FloatColumn,
	ColumnType.STRING:StringColumn,
	ColumnType.DATE:DateColumn,
	ColumnType.DATE_TIME:DateTimeColumn,
	ColumnType.TIME:TimeColumn,
	ColumnType.DAY_INTERVAL:DayIntervalColumn,
	ColumnType.JSON:JSONColumn,
}
