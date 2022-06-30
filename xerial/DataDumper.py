from xerial.DBSessionPool import DBSessionPool

import importlib, json, logging

class DataDumper :
	def __init__(self, config) :
		self.config = config
		self.pool = DBSessionPool(config)
		self.moduleName = self.config["dump"]['module']
		self.outputPath = self.config["dump"]['outputPath']
	
	def dump(self) :
		module = importlib.import_module(self.moduleName)
		self.pool.createConnection()
		self.session = self.pool.getSession()
		self.pool.browseModel(self.session, module=module)
		self.session.getExistingTable()

		for table, model in self.session.model.items() :
			# if table not in {"ReportName"} : continue
			logging.info(f">>> Dumping {table}.")
			recordList = self.session.select(model, "")
			dataList = [i.toDict() for i in recordList]
			path = f"{self.outputPath}/{table}.json"
			with open(path, "wt") as fd :
				json.dump(dataList, fd)
			logging.info(f">>> {table} of {len(dataList)} are dumped.")