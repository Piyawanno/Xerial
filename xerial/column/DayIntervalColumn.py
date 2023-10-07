from xerial.column.TimeColumn import TimeColumn
from xerial.constant.Vendor import Vendor

class DayIntervalColumn (TimeColumn) :
	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE :
			return "INTERVAL DAY TO SECOND"
		else :
			return "TIME"
	