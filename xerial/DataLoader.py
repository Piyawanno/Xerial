from xerial.DBSessionPool import DBSessionPool
from xerial.DBSessionBase import PrimaryDataError

import importlib, json, traceback, mariadb, logging

__CHUNKED__ = 1

class DataLoader :
	def __init__(self, config) :
		self.config = config
		self.pool = DBSessionPool(config)
		self.moduleName = self.config["load"]['module']
		self.inputPath = self.config["load"]['inputPath']
	
	def load(self) :
		module = importlib.import_module(self.moduleName)
		self.pool.createConnection()
		self.session = self.pool.getSession()
		self.pool.browseModel(self.session, module=module)
		self.session.getExistingTable()
		self.session.createTable()

		for table, model in self.session.model.items() :
			# if table not in {"ServiceType"} : continue
			logging.info(f">>> Loading {table}.")
			path = f"{self.inputPath}/{table}.json"
			with open(path, "rt") as fd :
				dataList = json.load(fd)
			
			n = 0
			for data in dataList :
				try :
					record = model().fromDict(data)
				except ValueError as error :
					record = None
				if record is not None :
					try :
						self.session.insert(record, isAutoID=False)
						n += 1
					except PrimaryDataError as error :
						logging.error("*** Error primary key cannot be null.")
			
			logging.info(f">>> {table} of {n}/{len(dataList)} are loaded.")
			