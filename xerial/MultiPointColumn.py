from xerial.Column import Column

import shapely.wkt, traceback, logging

# NOTE : Due to data in DB from Absolute Co.,Ltd. x and y are confound.
class MultiPointColumn (Column) :
	def fromDict(self, data) :
		return data.get(self.name, [])

	def processValue(self, raw):
		pointList = []
		if raw is None : return []
		try :
			data = shapely.wkt.loads(raw)
			pointList = []
			for i in data.geoms :
				pointList.append([i.y, i.x])
		except :
			logging.error(traceback.format_exc())
		return pointList
	
	def setValueToDB(self, attribute) :
		textList = ["(%f %f)"%(i[1], i[0]) for i in attribute]
		return "PointFromText('MULTIPOINT(%s)')"%(",".join(textList))

	def parseSelect(self) :
		return f'ST_AsText({self.name})'
	
	def getDBDataType(self) :
		return "MULTIPOINT"