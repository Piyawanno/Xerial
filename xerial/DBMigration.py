from xerial.AsyncDBSessionPool import AsyncDBSessionPool
from xerial.AsyncDBSessionBase import AsyncDBSessionBase

from typing import List, Dict, Callable

import importlib, os, json

__MAX__ = 1_000

Transfer = Callable[[List[Dict]], List[Dict]]

def nullTransfer(raw:List[Dict]) -> List[Dict] :
	return raw
class DBMigration :
	def __init__(self, config) :
		self.config = config
		self.pool:AsyncDBSessionPool = AsyncDBSessionPool(config)
		self.session:AsyncDBSessionBase = None
	
	async def connect(self, moduleList:List[str]) :
		await self.pool.createConnection()
		self.session = await self.pool.getSession()
		for i in moduleList :
			module = importlib.import_module(i)
			await AsyncDBSessionPool.browseModel(self.session, module)
		await self.session.getExistingTable()
		await self.session.createTable()
	
	async def close(self) :
		await self.pool.close()

	async def load(self, dataPath:str, transfer:Transfer=nullTransfer) :
		if os.path.isfile(dataPath) :
			await self.loadData(dataPath, transfer)
		elif os.path.isdir(dataPath) :
			for i in os.listdir(dataPath, transfer) :
				await self.loadData(f"{dataPath}/{i}")
		else :
			raise IOError(f"Path {dataPath} does not exist.")

	async def loadData(self, path:str, transfer:Transfer=nullTransfer) :
		name = os.path.basename(path)
		splitted = name.split(".")
		modelName = splitted[0]
		model = self.session.model.get(modelName, None)
		if model is None  :
			print(f"*** Warning : model {modelName} cannot be found.")
			return
		with open(path, "rt") as fd :
			raw = json.load(fd)
		recordList = [model().fromDict(transfer(i)) for i in raw]
		await self.session.dropByCondition(model, 'id > 0')
		await self.session.insertMultiple(recordList, isAutoID=False)
		primary = model.primary
		table = model.__full_table_name__
		maxID = max([getattr(i, primary) for i in recordList])
		query = f"ALTER SEQUENCE {table}_{primary}_seq RESTART {maxID+1};"
		await self.session.executeWrite(query)
		if len(raw) > 0 :
			print(f">>> {modelName} of {len(raw)} are loaded.")
	
	async def dump(self, dataPath:str, transfer:Transfer=nullTransfer) :
		if not os.path.isdir(dataPath) :
			raise IOError(f"Path {dataPath} is not a directory.")
		
		for model in self.session.model.values() :
			total = 0
			with open(f"{dataPath}/{model.__name__}.json", "wt") as fd :
				offset = 0
				clause = f"ORDER BY {model.primary}"
				while True :
					recordList = await self.session.select(model, clause, limit=__MAX__, offset=offset)
					total += len(recordList)
					if len(recordList) == 0 : break
					raw = [transfer(i.toDict()) for i in recordList]
					if offset > 0 :
						for i in raw :
							fd.write(",\n")
							json.dump(i, fd, indent=4, ensure_ascii=False)
					else :
						fd.write("[")
						for i in raw[:-1] :
							json.dump(i, fd, indent=4, ensure_ascii=False)
							fd.write(",\n")
						json.dump(raw[-1], fd, indent=4, ensure_ascii=False)
					offset += len(recordList)
				if offset > 0 : fd.write("]")
			if total > 0 :
				print(f">>> {model.__name__} of {total} are dumped.")
