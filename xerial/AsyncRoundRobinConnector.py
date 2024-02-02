from xerial.RoundRobinConnector import RoundRobinConnector

class AsyncRoundRobinConnector (RoundRobinConnector) :
	async def connect(self, hasCursor=True) :
		from xerial.AsyncDBSessionPool import AsyncDBSessionPool
		self.reader = []
		self.writer = None
		self.readerCursor = []
		self.writerCursor = None
		for i in self.config['connectionList'] :
			i['vendor'] = self.config['vendor']
			connector = await AsyncDBSessionPool.connect(i)
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
		self.isOpened = True
	
	async def close(self) :
		for i in self.reader :
			await i.close()
		self.isOpened = False