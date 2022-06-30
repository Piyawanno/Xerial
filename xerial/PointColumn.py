from xerial.Column import Column


# NOTE : Due to data in DB from Absolute Co.,Ltd. x and y are confound.
class PointColumn (Column) :
	def fromDict(self, data) :
		return data.get(self.name, [])
		
	def processValue(self, raw):
		splitted = raw[6:-1].split(' ')
		x = float(splitted[1])
		y = float(splitted[0])
		return [x, y]
	
	def setValueToDB(self, attribute) :
		return f"PointFromText('POINT({attribute[1]} {attribute[0]})')"
	
	def getDBDataType(self) :
		return "POINT"

	def parseSelect(self) :
		return f'ST_AsText({self.name})'