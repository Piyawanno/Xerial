from xerial.AsyncDBSessionPool import AsyncDBSessionPool
from xerial.Record import Record

from typing import List

import argparse, json, asyncio, importlib, os, sys

def run():
	XerialModelExtratorCLI().run(sys.argv[1:])

class XerialModelExtratorCLI:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description="Xerial Model Meta Data Extraction")
		self.parser.add_argument("-c", "--connection", help="Path for connection configuration.")
		self.parser.add_argument("-m", "--module", help="Module to browse model.")
		self.parser.add_argument("-o", "--out", help="Output of browsed model.")

	def run(self, argv: List[str]):
		self.option = self.parser.parse_args(argv)
		self.config = XerialModelExtratorCLI.loadConfig()
		asyncio.run(self.extract(self.option.module, self.option.out))
	
	def browseModule(path: str) :
		for i in os.listdir(path):
			if i[-3:] != '.py' or i == "__init__.py" or os.path.isdir(f"{path}/{i}"): continue
			yield i[:-3]
	
	def importModule(self, moduleName: str):
		module = importlib.import_module(moduleName)
		for i in module.__path__ :
			if not os.path.isdir(i) : continue
			for name in self.browseModule(i) :
				module = importlib.import_module(f'{moduleName}.{name}')
				modelClass = getattr(module, name)
				if modelClass is None:
					continue
				if issubclass(modelClass, Record):
					self.session.appendModel(modelClass)
			break

	async def extract(self, moduleName: str, outputPath: str):
		self.pool = AsyncDBSessionPool(self.config)
		await self.pool.createConnection()
		self.session = await self.pool.getSession()
		self.importModule(moduleName)
		
		result = []
		for name, model in self.session.model.items() :
			columnList = []
			for i, meta in model.meta :
				columnList.append({
					'name' : i,
					'columnType' : meta.__class__.__name__,
					'foreignKey' : None if meta.foreignKey is None else meta.foreignKey.reference,
				})
			result.append({
				'modelName' : name,
				'column' : columnList
			})
		with open(outputPath, 'wt') as fd :
			json.dump(result, fd, indent=4)
	
	@staticmethod
	def loadConfig() -> dict:
		with open('/etc/xerial/Xerial.json', 'rt') as fd :
			config = json.load(fd)
		return config

if __name__ == '__main__': run()