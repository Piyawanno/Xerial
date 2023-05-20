import logging

"""
NOTE

RoundRobinConnector is designed for the case of Replication.
The read cursor/connector to each Read-Replica will be iterated
with RoundRobin algorithm. There is, however, only one write connector.
Since the most DB support one active Replica.
"""
class RoundRobinConnector :
	def __init__(self, config:dict) :
		self.config = config
		self.reader = []
		self.writer = None
		self.readerCursor = []
		self.writerCursor = None
	
	def connect(self, hasCursor=True) :
		from xerial.DBSessionPool import DBSessionPool
		self.reader = []
		self.writer = None
		self.readerCursor = []
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
				self.readerCursor.append(cursor)

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
		cursor = self.readerCursor[self.i]
		self.i = self.i+1
		if self.i >= self.n : self.i = 0
		return cursor
	
	def close(self) :
		for i in self.reader :
			i.close()
