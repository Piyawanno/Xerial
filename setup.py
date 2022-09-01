#!/usr/bin/python3

import os, sys, site, getpass, setuptools

class XerialSetup :
	def __init__(self) :
		self.rootPath = os.path.dirname(os.path.abspath(__file__))
		self.sitePackagesPath = ''
		for path in site.getsitepackages()[::-1]:
			if os.path.isdir(path): 
				self.sitePackagesPath = path
				break

	def operate(self, operation) :
		if operation == 'setup' :
			self.setup()
		elif operation == 'link' :
			self.link()
		elif operation == 'install' :
			self.install()
		elif operation == 'bdist_wheel' :
			self.createWheel()
	
	def createWheel(self) :
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
			python_requires='>=3.8',
		)

	def setup(self):
		self.setupBase()
		self.setupPIP()
	
	def setupBase(self) :
		if 'oracle' in sys.argv :
			with open('requirements-centos.txt') as fd :
				content = fd.read()
			self.setupYum(content.replace("\n", " "))
		elif 'debian10' in sys.argv or 'ubuntu20.04' in sys.argv:
			with open('requirements-ubuntu-20.04.txt') as fd :
				content = fd.read()
			self.setupAPT(content.replace("\n", " "))
		else :
			print("*** Error Not support for platform")
			print("*** Supported platform : debian10, ubuntu20.04, oracle")
			print("*** Example : ./setup.py setup debian10")

	def setupAPT(self, packageList) :
		command = 'apt-get install %s'%(" ".join(packageList))
		print(command)
		os.system(command)

	def setupPIP(self) :
		print(">>> Installing pip package.")
		with open('requirements.txt') as fd :
			content = fd.read()
		command = "pip3 install %s"%(content.replace("\n", " "))
		print(command)
		os.system(command)
	
	def link(self) :
		# self.installConfig()
		self.installScript()
		command = [
			"ln -s %s/xerial %s/xerial"%(self.rootPath, self.sitePackagesPath),
		]
		for i in command :
			print(i)
			os.system(i)

	def install(self) :
		print(">>> Installing Xerial.")
		if '-s' not in sys.argv : self.installConfig()
		else : os.system('cp config/Xerial.json /etc/xerial/')
		self.installScript()
		path = "/var/katatong"
		if not os.path.isdir(path) :
			os.makedirs(path)
		packagePath = self.sitePackagesPath+'/xerial'
		if not os.path.isdir(packagePath) :
			os.makedirs(packagePath)
		command = [
			"cp -rfv %s/xerial/* %s"%(self.rootPath, packagePath),
		]
		for i in command :
			print(i)
			os.system(i)
	
	def installConfig(self) :
		if os.path.isfile("/etc/xerial/Xerial.json") :
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
		command = [
			"ln -s %s/script/xerial-generate /usr/bin"%(self.rootPath),
			"ln -s %s/script/xerial-dump /usr/bin"%(self.rootPath),
			"ln -s %s/script/xerial-load /usr/bin"%(self.rootPath),
		]
		for i in command :
			print(i)
			os.system(i)
	
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
    setup = XerialSetup()
    setup.operate(sys.argv[-1])

