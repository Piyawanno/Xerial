from enum import IntEnum
from xerial.IntegerColumn import IntegerColumn
from xerial.FloatColumn import FloatColumn
from xerial.StringColumn import StringColumn
from xerial.DateColumn import DateColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.TimeColumn import TimeColumn
from xerial.DayIntervalColumn import DayIntervalColumn
from xerial.JSONColumn import JSONColumn

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
