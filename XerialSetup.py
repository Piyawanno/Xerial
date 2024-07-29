#!/usr/bin/python3

import os, sys, site, getpass
from re import I

__help__ = """Xerial setup script :
setup : Install dependencies of Xerial.
install : Install Xerial into machine.
link : Link package and script into machine, suitable for setting up developing environment.
bdist_wheel : Build wheel file into ./dist
"""


def __conform__(path) :
	isRootPath = False
	splited = path.split("/")
	if len(splited) <= 1: return path
	rootPrefix = ('etc', 'var', 'usr')
	if splited[1] in rootPrefix: isRootPath = True
	if sys.platform == 'win32':
		from pathlib import Path
		result = os.sep.join([i for i in splited if len(i)])
		if isRootPath: result = str(Path.home()) + os.sep + result
		if path[-1] == "/": result = result + os.sep
		return result
	result = "/"+("/".join([i for i in splited if len(i)]))
	if path[-1] == "/": result = result + "/"
	return result


def __link__(source, destination):
	source = __conform__(source)
	destination = __conform__(destination)
	command = f"ln -s {source} {destination}"
	if sys.platform == 'win32': command = f"mklink /D {destination} {source}"
	print(command)
	os.system(command)

class XerialSetup :
	def __init__(self) :
		self.rootPath = os.path.dirname(os.path.abspath(__file__))
		self.sitePackagesPath = ''
		for path in site.getsitepackages()[::-1]:
			if os.path.isdir(path):
				self.sitePackagesPath = path
				break
		
		self.script = [
			'xerial-dump',
			'xerial-raw-dump',
			'xerial-generate',
			'xerial-load',
			'xerial-model-extract',
			'xerial-primary',
		]

		self.configList = [
			(f'DBMigration.example.json', 'DBMigration.json'),
		]

		self.installPathList = [
			(f"{self.rootPath}/xerial", f"{self.sitePackagesPath}/xerial"),
		]

		self.copyCommand = 'cp'
		if sys.platform == 'win32': self.copyCommand = "copy"

	def operate(self, operation, platform) :
		if operation == 'setup' :
			self.setup(platform)
		elif operation == 'link' :
			self.link()
		elif operation == 'install' :
			self.install()
		elif operation == 'bdist_wheel' :
			self.createWheel()
	
	def createWheel(self) :
		import setuptools
		with open("README.md") as fd :
			description = fd.read()
		
		with open("requirements.txt") as fd :
			requires = fd.read().split("\n")

		setuptools.setup(
			name="xerial",
			version="0.9",
			author="Kittipong Piyawanno",
			author_email="k.piyawanno@gmail.com",
			description="A Simple Object Rational Mapping (ORM) library",
			long_description=description,
			long_description_content_type="text/markdown",
			packages=setuptools.find_packages(),
			install_requires=requires,
			classifiers=[
				"Programming Language :: Python :: 3",
				"Development Status :: 3 - Alpha",
				"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
				"Operating System :: OS Independent",
				"Topic :: Database",
			],
			scripts=[f'script/{i}' for i in self.script],
			python_requires='>=3.8',
		)

	def setup(self, platform):
		self.setupBase(platform)
		self.setupPIP()
	
	def setupBase(self, platform) :
		if 'oracle' in platform or 'centos' in platform:
			with open('requirements-centos.txt') as fd :
				content = fd.read()
			self.setupYum(content.replace("\n", " "))
		elif 'debian10' in platform or 'ubuntu20.04' in platform:
			with open('requirements-ubuntu-20.04.txt') as fd :
				content = fd.read()
			self.setupAPT(content.split("\n"))
		else :
			print("*** Error Not support for platform")
			print("*** Supported platform : debian10, ubuntu20.04, oracle")
			print("*** Example : ./setup.py setup debian10")

	def setupAPT(self, packageList) :
		command = 'apt-get install -y %s'%(" ".join(packageList))
		print(command)
		os.system(command)

	def setupPIP(self) :
		print(">>> Installing pip package.")
		with open('requirements.txt') as fd :
			content = fd.read()
		command = "pip3 install %s"%(content.replace("\n", " "))

		import platform
		subversion = int(platform.python_version().split('.')[1])
		if subversion >= 11:
			command = "pip3 install --break-system-packages %s"%(content.replace("\n", " "))
		else:
			command = "pip3 install %s"%(content.replace("\n", " "))

		print(command)
		os.system(command)
	
	def link(self) :
		self.installConfig()
		self.installScript()
		
		for source, destination in self.installPathList  :
			destination = __conform__(destination)
			source = __conform__(source)
			if not os.path.isdir(destination) :
				__link__(source, destination)

	def install(self) :
		print(">>> Installing Xerial.")
		self.installConfig()
		self.installScript()
		for source, destination in self.installPathList  :
			destination = __conform__(destination)
			source = __conform__(source)
			if not os.path.isdir(destination) :
				os.makedirs(destination)
			command = f"{self.copyCommand} -fR {source} {destination}"
			print(command)
			os.system(command)
	
	def installConfig(self) :
		path = __conform__("/etc/xerial")
		if not os.path.exists(path): os.makedirs(path)
		for source, destination in self.configList :
			destinationPath = __conform__(f"{path}/{destination}")
			if not os.path.isfile(destinationPath) :
				sourcePath = __conform__(f"{self.rootPath}/config/{source}")
				command = f"{self.copyCommand} {sourcePath} {destinationPath}"
				print(command)
				os.system(command)
		self.installConnectionConfig()
	
	def installConnectionConfig(self) :
		if os.path.isfile("/etc/xerial/Xerial.json") :
			if not os.path.isfile("/etc/gaimon/Database.json"):
				__link__("/etc/xerial/Xerial.json", "/etc/gaimon/Database.json")
			return
		path = "/etc/xerial"
		if not os.path.isdir(path) :
			os.makedirs(path)
		parameter = self.getParameter()
		with open("%s/config/Xerial.example.json"%(self.rootPath), "rt") as source :
			raw = source.read()
			raw = raw.replace('"DB_PORT"', "DB_PORT")
			raw = raw.replace('"DB_VENDOR"', "DB_VENDOR")
			for k, v in parameter.items() :
				raw = raw.replace(k, v)
			with open("/etc/xerial/Xerial.json", "wt") as target :
				target.write(raw)
	
	def installScript(self) :
		for i in self.script :
			if not os.path.isfile(f"/usr/bin/{i}") :
				__link__(f"{self.rootPath}/script/{i}", f"/usr/bin/{i}")

	def getParameter(self) :
		parameter = {}
		parameter['DB_HOST'] = input("DB host : ")
		parameter['DB_PORT'] = input("DB port : ")
		parameter['DB_NAME'] = input("DB : ")
		parameter['DB_USER'] = input("DB user : ")
		parameter['DB_PASSWORD'] = getpass.getpass("DB password : ")
		vendor = input("DB vendor (1=PostgeSQL, 2=MariaDB, 3=MySQL, 4=Oracle) : ")
		try :
			vendor = int(vendor)
			if vendor > 4 :
				print("*** Warning : Vendor %d is not defined, will be set to MariaDB."%(vendor))
				parameter['DB_VENDOR'] = "2"
			else :
				parameter['DB_VENDOR'] = str(vendor)
		except :
			print("*** Warning : Vedor cannot be parsed, will be set to MariaDB.")
			parameter['DB_VENDOR'] = "2"
		if parameter['DB_VENDOR'] == "4" :
			parameter['DB_DOMAIN'] = input("DB domain : ")
		
		return parameter
	

if __name__ == '__main__' :
	from argparse import RawTextHelpFormatter
	import argparse
	parser = argparse.ArgumentParser(description=__help__, formatter_class=RawTextHelpFormatter)
	parser.add_argument("operation", help="Operation of setup", choices=['setup', 'install', 'link', 'bdist_wheel'])
	parser.add_argument("-p", "--platform", help="Platform for installation of base environment.", choices=['oracle', 'centos', 'debian10', 'ubuntu20.04'])
	option = parser.parse_args(sys.argv[1:])
	if option.platform is None : option.platform = 'ubuntu20.04'
	setup = XerialSetup()
	setup.operate(option.operation, option.platform)

