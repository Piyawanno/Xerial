from xerial.RoundRobinConnector import RoundRobinConnector

class AsyncRoundRobinConnector (RoundRobinConnector) :
	async def connect(self, hasCursor=True) :
		from xerial.AsyncDBSessionPool import AsyncDBSessionPool
		self.reader = []
		self.writer = None
		self.readerCurosr = []
		self.writerCursor = None
		for i in self.config['connectionList'] :
			i['vendor'] = self.config['vendor']
			connector = await AsyncDBSessionPool.connect(i)
			if i.get('isWrite', False) : self.writer = connector
			self.reader.append(connector)
			if hasCursor :
				cursor = connector.cursor()
				if isWrite : self.writerCursor = cursor
				self.readerCurosr.append(cursor)
		if self.writer is None :
			raise ValueError("No write connector is defined.")
		self.i = 0
		self.n = len(self.reader)
	
	async def close(self) :
		for i in self.reader :
			await i.close()