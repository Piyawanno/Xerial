from xerial.FloatColumn import FloatColumn
from datetime import timedelta
from typing import List

class TimeIntervalColumn (FloatColumn) :
	def __init__(self,
			isNotNull=False,
			default=None,
			foreignKey=None,
			isIndex=False,
			isRepresentative=False,
			parentModel:List[type]=[],
			input=None) :
			
		FloatColumn.__init__(self,
			isPrimary=False,
			length=32,
			isNotNull=isNotNull,
			default=default,
			foreignKey=foreignKey,
			isIndex=isIndex,
			isRepresentative=isRepresentative,
			parentModel=parentModel,
			input=input
		)
		self.precision = 8
	
	def toDict(self, attribute):
		return attribute.total_seconds()

	def fromDict(self, data) :
		return data.get(self.name, self.default)

	def processValue(self, raw):
		if raw is None: return None
		return timedelta(seconds=float(raw))

	def setValueToDB(self, attribute:timedelta) :
		return str(attribute.seconds)

	def parseValue(self, value) :
		return timedelta(seconds=float(value))
