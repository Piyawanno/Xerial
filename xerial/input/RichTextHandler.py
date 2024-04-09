class RichTextHandler:
	def __init__(self, name:str, url:str):
		self.name = name
		self.url = url
	
	def toDict(self):
		return {
			'name': self.name,
			'url': self.url,
		}