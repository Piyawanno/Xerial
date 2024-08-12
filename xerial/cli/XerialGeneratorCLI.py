from xerial.Vendor import Vendor

from typing import List

import json, argparse, sys

def run():
	XerialGeneratorCLI().run(sys.argv[1:])

class XerialGeneratorCLI:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description="Xerial-Generator : Generate Model source code from existing DB scheme.")

	def run(self, argv: List[List]):
		self.option = self.parser.parse_args(argv)
		self.config = XerialGeneratorCLI.loadConfig()
		self.generate()
	
	def generate(self):
		vendor = self.config['vendor']
		if vendor != Vendor.ORACLE:
			print("*** WARNING Support only Oracle DB.")
			return
		from xerial.OracleModelGenerator import OracleModelGenerator
		self.generator = OracleModelGenerator(self.config)
		self.generator.connect()
		language = self.config['generator']['outputLanguage']
		if language == 'JavaScript' :
			self.generator.generateJS()
		elif language == 'Python' :
			self.generator.generatePython()
		else :
			print("*** Error : Language %s is not supported."%(language))

	@staticmethod
	def loadConfig() -> dict:
		with open('/etc/xerial/Xerial.json', 'rt') as fd :
			config = json.load(fd)
		return config

if __name__ == '__main__': run()