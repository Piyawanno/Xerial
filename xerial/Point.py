from math import pi, sin, asin, cos, atan2, sqrt

__RADIAN__ = pi/180.0
__RADIUS__ = 6371.01

class Point :
	def __init__(self, latitude=0.0, longitude=0.0) :
		self.latitude = latitude
		self.longitude = longitude
	
	@staticmethod
	def getSphereDistance(lon1, lat1, lon2, lat2):
		lon1, lat1, lon2, lat2 = lon1*__RADIAN__, lat1*__RADIAN__, lon2*__RADIAN__, lat2*__RADIAN__
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		return __RADIUS__*(2 * atan2(sqrt(a), sqrt(1-a)))
	
	@staticmethod
	def getNextSpherePoint(lon1, lat1, course, distance):
		lon1 = __RADIAN__*lon1
		lat1 = __RADIAN__*lat1
		course = __RADIAN__*course
		distance = distance/21851.944728932118
		
		lat2 = asin(sin(lat1)*cos(distance) + cos(lat1)*sin(distance)*cos(course))
		lon2 = lon1 + atan2(sin(course)*sin(distance)*cos(lat1), cos(distance)-sin(lat1)*sin(lat2))
		return lon2/__RADIAN__, lat2/__RADIAN__

