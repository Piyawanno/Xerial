from xerial.DBSessionBase import DBSessionBase
from xerial.RoundRobinConnector import RoundRobinConnector
from xerial.Vendor import Vendor
from xerial.Record import Record

import traceback, importlib, os, logging, time

class DBSessionPool :
	def __init__(self, config, model:dict=None):
		self.config = config
		self.isRoundRobin = config.get("isRoundRobin", False)
		if self.isRoundRobin : self.callConnector = DBSessionPool.connectRoundRobin
		else : self.callConnector = DBSessionPool.connect
		self.pool = []
		self.connectionCount = 0
		self.connectionNumber = config.get("connectionNumber", 8)
		self.model = model
		self.schema = None
		self.connection = []
		self.vendor = config["vendor"]
		if self.vendor == Vendor.MARIADB :
			from xerial.MariaDBSession import MariaDBSession
			self.sessionInstance = MariaDBSession
		elif self.vendor == Vendor.ORACLE :
			from xerial.OracleDBSession import OracleDBSession
			self.sessionInstance = OracleDBSession
		elif self.vendor == Vendor.POSTGRESQL :
			from xerial.PostgresDBSession import PostgresDBSession
			self.sessionInstance = PostgresDBSession
		elif self.vendor == Vendor.SQLITE :
			from xerial.SQLiteDBSession import SQLiteDBSession
			self.sessionInstance = SQLiteDBSession
		elif self.vendor == Vendor.MSSQL :
			from xerial.MSSQLDBSession import MSSQLDBSession
			self.sessionInstance = MSSQLDBSession
	
	def setSchema(self, schema:str) :
		if self.vendor != Vendor.POSTGRESQL :
			raise ValueError("Only PostgreSQL supports schema.")
		self.schema = schema
	
	def createConnection(self) :
		self.connection = []
		for i in range(self.connectionNumber) :
			session = self.sessionInstance(self.config)
			session.connect()
			if self.schema is not None :
				session.setSchema(self.schema)
			self.pool.append(session)
	
	def reconnectDB(self) :
		session = self.sessionInstance(self.config)
		session.connect()
		if self.schema is not None :
			session.setSchema(self.schema)
		if self.model is None :
			self.model = session.model
		else :
			session.model = self.model
		return session
	
	def getSession(self) -> DBSessionBase :
		while True :
			if len(self.pool) == 0 :
				time.sleep(0.0001)
			else :
				session = self.pool.pop()
				return session
	
	def release(self, session) :
		if len(self.pool) < self.connectionNumber :
			self.pool.append(session)
		else :
			session.closeConnection()
	
	def close(self) :
		logging.info(">>> Closing Connections %s"%(self.config["database"]))
		for session in self.pool :
			try :
				session.closeConnection()
			except :
				logging.error(traceback.format_exc())
	
	@staticmethod
	def browseModel(session, module) :
		path = list(module.__path__)[0]
		baseName = module.__name__
		for i in os.listdir(path) :
			if i[-3:] != '.py' or i == "__init__.py" or os.path.isdir("%s/%s"%(path, i)) : continue
			name = i[:-3]
			try :
				module = importlib.import_module('%s.%s'%(baseName, name))
				modelClass = getattr(module, name)
				if issubclass(modelClass, Record) :
					session.appendModel(modelClass)
			except Exception as error :
				logging.error(traceback.format_exc())
				raise error

	@staticmethod
	def connect(config) :
		vendor = config["vendor"]
		if vendor == Vendor.MARIADB :
			try :
				import mariadb
			except :
				logging.warning("*** Warning MariaDB cannot be imported.")
			return mariadb.connect(
				user=config["user"],
				password=config["password"],
				host=config["host"],
				port=config["port"],
				database=config["database"]
			)
		elif vendor == Vendor.ORACLE :
			try :
				import cx_Oracle
			except :
				logging.warning("*** Warning OracleDB cannot be imported.")
			connectionString = '%s/%s@%s:%d'%(
				config['user'],
				config["password"],
				config["host"],
				config["port"],
				config["domain"],
			)
			connection = cx_Oracle.connect(connectionString)
			connection.autocommit = True
			return connection
		elif vendor == Vendor.POSTGRESQL :
			try :
				import psycopg2
			except :
				logging.warning("*** Warning PostgreSQL cannot be imported.")
			connection = psycopg2.connect(
				user=config["user"],
				password=config["password"],
				host=config["host"],
				port=config["port"],
				database=config["database"]
			)
			connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
			return connection
		elif vendor == Vendor.SQLITE :
			import sqlite3
			return sqlite3.connect(config["database"], isolation_level=None, check_same_thread=False)
		elif vendor == Vendor.MSSQL :
			try :
				import pyodbc
			except :
				logging.warning("Module pyodbc cannot be imported.")

			connection = pyodbc.connect(f"""
				DRIVER={{{config['driver']}}};
				SERVER={config['host']};
				DATABASE={config['database']};
				UID={config['user']};
				PWD={config['password']};
				TrustServerCertificate=yes;
			""", autocommit=True)
			return connection

		else :
			raise ValueError("Vendor %d is not supported yet."%(vendor))

	@staticmethod
	def connectRoundRobin(config) :
		connector = RoundRobinConnector(config)
		connector.connect(True)
		return connector