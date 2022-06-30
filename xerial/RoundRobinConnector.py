import logging

class RoundRobinConnector :
	def __init__(self, config:dict) :
		self.config = config
		self.reader = []
		self.writer = None
		self.readerCurosr = []
		self.writerCursor = None
	
	def connect(self, hasCursor=True) :
		from xerial.DBSessionPool import DBSessionPool
		self.reader = []
		self.writer = None
		self.readerCurosr = []
		self.writerCursor = None
		for i in self.config['connectionList'] :
			i['vendor'] = self.config['vendor']
			connector = DBSessionPool.connect(i)
			isWrite = i.get('isWrite', False)
			if isWrite : self.writer = connector
			self.reader.append(connector)
			if hasCursor :
				cursor = connector.cursor()
				if isWrite : self.writerCursor = cursor
				self.readerCurosr.append(cursor)

		if self.writer is None :
			raise ValueError("No write connector is defined.")
		self.i = 0
		self.n = len(self.reader)
	
	def getNextRead(self) :
		connector = self.reader[self.i]
		self.i = self.i+1
		if self.i >= self.n : self.i = 0
		return connector
	
	def getNextReadCursor(self) :
		cursor = self.readerCurosr[self.i]
		self.i = self.i+1
		if self.i >= self.n : self.i = 0
		return cursor
	
	def close(self) :
		for i in self.reader :
			i.close()
