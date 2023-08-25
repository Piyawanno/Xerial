from xerial.AsyncDBSessionPool import AsyncDBSessionPool
from xerial.AsyncDBSessionBase import AsyncDBSessionBase

from typing import List, Dict, Callable

import os, json

__MAX__ = 1_000

Transfer = Callable[[List[Dict]], List[Dict]]

def nullTransfer(raw:List[Dict]) -> List[Dict] :
	return raw

class RawMigration :
	def __init__(self, config) :
		self.config = config
		self.pool:AsyncDBSessionPool = AsyncDBSessionPool(config)
		self.session:AsyncDBSessionBase = None
	
	async def connect(self) :
		await self.pool.createConnection()
		self.session = await self.pool.getSession()
	
	async def close(self) :
		await self.pool.close()

	async def dump(self, dataPath:str, transfer:Transfer=nullTransfer) :
		if not os.path.isdir(dataPath) :
			raise IOError(f"Path {dataPath} is not a directory.")
		
		existingTable = await self.session.getExistingTable()
		for table in existingTable :
			offset = 0
			path = f"{dataPath}/{table}.json"
			with open(path, "wt") as fd :
				while True :
					query = self.session.generateRawSelectQuery(table, "", __MAX__, offset)
					result = await self.session.selectRaw(query)
					if len(result) == 0 : break
					if offset > 0 :
						for i in result :
							fd.write(",\n")
							json.dump(i, fd, indent=4, ensure_ascii=False)
					else :
						fd.write("[")
						for i in result[:-1] :
							json.dump(i, fd, indent=4, ensure_ascii=False)
							fd.write(",\n")
						json.dump(result[-1], fd, indent=4, ensure_ascii=False)
					offset += len(result)
				if offset > 0 : fd.write("]")
			print(f">>> Dump {table} of {offset}.")
		print(">>> FINISH DUMP")
				