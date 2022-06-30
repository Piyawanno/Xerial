from xerial.TimeColumn import TimeColumn, TIME_FORMAT
from xerial.Vendor import Vendor

class DayIntervalColumn (TimeColumn) :
	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE :
			return "INTERVAL DAY TO SECOND"
		else :
			return "TIME"
	