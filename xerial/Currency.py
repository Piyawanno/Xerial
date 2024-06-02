import os, json

class Currency :
	symbol: str
	name: str
	symbolNative: str
	decimalDigits: int
	rounding: int
	code: str
	namePlural: str

	def __repr__(self) -> str:
		return self.code

	def fromDict(self, raw) :
		self.symbol = raw["symbol"]
		self.name = raw["name"]
		self.symbolNative = raw["symbol_native"]
		self.decimalDigits = raw["decimal_digits"]
		self.rounding = raw["rounding"]
		self.code = raw["code"]
		self.namePlural = raw["name_plural"]
		return self
	
	def toDict(self) :
		return {
			"symbol" : self.symbol,
			"name" : self.name,
			"symbol_native" : self.symbolNative,
			"decimal_digits" : self.decimalDigits,
			"rounding" : self.rounding,
			"code" : self.code,
			"name_plural" : self.namePlural,
		}

	@staticmethod
	def loadData() :
		path = os.path.dirname(os.path.abspath(__file__))
		dataPath = f'{path}/data/Common-Currency.json'
		with open(dataPath, encoding='utf-8') as fd:
			raw = json.load(fd)
			loaded = {k:Currency().fromDict(v) for k,v in raw.items()}
		return loaded

