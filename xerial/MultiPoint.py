from xerial.Point import Point

class MultiPoint :
	def __init__(self) :
		self.pointList = []
	
	@staticmethod
	def calculateDistance(pointList) :
		if len(pointList) < 2 : return 0.0
		previous = pointList[0]
		distance = 0.0
		for i in pointList[1:] :
			distance += Point.getSphereDistance(
				previous[0], previous[1], i[0], i[1]
			)
			previous = i
		return distance
