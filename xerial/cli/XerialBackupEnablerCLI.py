from xerial.AsyncDBSessionPool import AsyncDBSessionPool

from typing import List

import argparse, json, asyncio, sys

def run():
	XerialBackupEnablerCLI().run(sys.argv[1:])

class XerialBackupEnablerCLI:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description="Xerial Primary Key Creator")
		self.parser.add_argument("-c", "--connection", help="Path for connection configuration.")

	def run(self, argv: List[str]):
		self.option = self.parser.parse_args(argv)
		self.config = XerialBackupEnablerCLI.loadConfig()
		asyncio.run(self.createPrimary())
	
	async def createPrimary(self):
		pool = AsyncDBSessionPool(self.config)
		await pool.createConnection()
		session = await pool.getSession()
		tableList = await session.getExistingTable()
		for table in tableList:
			query = f'ALTER TABLE {table} ADD __insert_time__ DOUBLE PRECISION;'
			print(query)
			try :
				await session.executeWrite(query)
			except:
				print(f"TABLE {table}.id cannot add __insert_time__.")
			
			query = f'ALTER TABLE {table} ADD __update_time__ DOUBLE PRECISION;'
			print(query)
			try :
				await session.executeWrite(query)
			except:
				print(f"TABLE {table}.id cannot add __update_time__.")

	@staticmethod
	def loadConfig() -> dict:
		with open('/etc/xerial/Xerial.json', 'rt') as fd :
			config = json.load(fd)
		return config

if __name__ == '__main__': run()