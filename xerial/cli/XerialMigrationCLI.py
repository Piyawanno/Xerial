from xerial.DBMigration import DBMigration
from xerial.RawMigration import RawMigration

from typing import List

import json, argparse, sys, asyncio

def runDump():
	XerialMigrationCLI("Xerial-Dump : dump data from DB into json file.").runDump(sys.argv[1:])

def runRawDump():
	XerialMigrationCLI("Xerial-Raw-Dump : dump data from DB into json file (Raw Mode no Model).").runRawDump(sys.argv[1:])


def runLoad():
	XerialMigrationCLI("Xerial-Dump : load data into DB from json file.").runLoad(sys.argv[1:])


class XerialMigrationCLI:
	def __init__(self, description: str):
		self.parser = argparse.ArgumentParser(description=description)
		self.parser.add_argument("-c", "--connection", help="Path for connection configuration.")
		self.parser.add_argument("-m", "--migration", help="Path for dump migration configuration.")

	def prepare(self, argv: List[str]):
		self.option = self.parser.parse_args(argv)
		self.config = XerialMigrationCLI.loadConfig(self.option.connection, self.option.migration)

	def runDump(self, argv: List[str]):
		self.prepare(argv)
		asyncio.run(self.dump())
	
	def runRawDump(self, argv: List[str]):
		self.prepare(argv)
		asyncio.run(self.dumpRaw())
	
	def runLoad(self, argv: List[str]):
		self.prepare(argv)
		asyncio.run(self.load())

	async def dump(self):
		self.migration = DBMigration(self.config['connection'])
		await self.migration.connect(self.config['migration']['model'])
		await self.migration.dump(self.config['migration']['dataPath'])
		await self.migration.close()
	
	async def dumpRaw(self):
		self.migration = RawMigration(self.config['connection'])
		await self.migration.connect()
		await self.migration.dump(self.config['migration']['dataPath'])
		await self.migration.close()
		
	async def load(self):
		self.migration = DBMigration(self.config['connection'])
		await self.migration.connect(self.config['migration']['model'])
		await self.migration.load(self.config['migration']['dataPath'])
		await self.migration.close()

	@staticmethod
	def loadConfig(connectionPath: str, migrationPath: str) -> dict:
		config = {}
		with open(connectionPath) as fd :
			config['connection'] = json.load(fd)

		with open(migrationPath) as fd :
			config['migration'] = json.load(fd)
		return config

if __name__ == '__main__': run()