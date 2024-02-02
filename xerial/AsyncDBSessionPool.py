from xerial.DBSessionPool import DBSessionPool
from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.AsyncRoundRobinConnector import AsyncRoundRobinConnector
from xerial.Vendor import Vendor
from xerial.Record import Record

import logging, traceback, os, importlib, asyncio, time

MAX_WAIT = 10_000
WAIT_TIME = 0.0001
class AsyncDBSessionPool (DBSessionPool) :
	def __init__(self, config, model:dict=None):
		super().__init__(config, model)
		if self.isRoundRobin : self.callConnector = AsyncDBSessionPool.connectRoundRobin
		else : self.callConnector = AsyncDBSessionPool.connect
		if self.vendor == Vendor.POSTGRESQL :
			from xerial.AsyncPostgresDBSession import AsyncPostgresDBSession
			self.sessionInstance = AsyncPostgresDBSession
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL :
			from xerial.AsyncMariaDBSession import AsyncMariaDBSession
			self.sessionInstance = AsyncMariaDBSession
		elif self.vendor == Vendor.ORACLE :
			from xerial.AsyncOracleDBSession import AsyncOracleDBSession
			self.sessionInstance = AsyncOracleDBSession
		elif self.vendor == Vendor.SQLITE :
			from xerial.AsyncSQLiteDBSession import AsyncSQLiteDBSession
			self.sessionInstance = AsyncSQLiteDBSession
		elif self.vendor == Vendor.MSSQL :
			from xerial.AsyncMSSQLDBSession import AsyncMSSQLDBSession
			self.sessionInstance = AsyncMSSQLDBSession
		self.maxConnectionTime = config.get('maxConnectionTime', 60*60*6)
		self.lastConnectionTime = -1.0
	
	async def createConnection(self) :
		for i in range(self.connectionNumber) :
			session = await self.reconnectDB()
			self.pool.append(session)
	
	async def reconnectDB(self) -> AsyncDBSessionBase :
		session = self.sessionInstance(self.config)
		await session.connect()
		if self.schema is not None :
			session.setSchema(self.schema)
		if self.model is None :
			self.model = session.model
		else :
			session.model = self.model
		return session
	
	async def getSession(self) -> AsyncDBSessionBase :	
		now = time.time()
		wait = 0
		while True :
			if len(self.pool) == 0 :
				if wait >= MAX_WAIT :
					logging.warning("*** Warning no Session left, create new session.")
					session: AsyncDBSessionBase = await self.reconnectDB()
					session.queryCount = 0
					return session
				else :
					await asyncio.sleep(WAIT_TIME)
			else :
				session: AsyncDBSessionBase = self.pool.pop()
				if not session.isOpened : continue
				if now - session.lastConnectionTime > self.maxConnectionTime :
					logging.info(">>> Reconnect Session")
					await session.closeConnection()
					await session.connect()
					session.lastConnectionTime = now
				session.queryCount = 0
				return session
			wait = wait + 1
	
	async def release(self, session: AsyncDBSessionBase) :
		if len(self.pool) < self.connectionNumber :
			self.pool.append(session)
		else :
			await session.closeConnection()

	async def close(self) :
		logging.info(">>> Closing Connections ")
		for session in self.pool :
			try :
				await session.closeConnection()
			except :
				logging.error(traceback.format_exc())
	
	@staticmethod
	async def browseModel(session, module) :
		path = list(module.__path__)[0]
		baseName = module.__name__
		for i in os.listdir(path) :
			if os.path.isdir("%s/%s"%(path, i)) and os.path.isfile(f"{path}/{i}/__init__.py") :
				for j in os.listdir("%s/%s"%(path, i)) :
					if j[-3:] != '.py' or j == "__init__.py" or os.path.isdir("%s/%s/%s"%(path, i,j)) : 
						pass
					else:
						name = j[:-3]
						try :
							module = importlib.import_module('%s.%s.%s'%(baseName,i, name))
							modelClass = getattr(module, name)
							if issubclass(modelClass, Record) :
								session.appendModel(modelClass)
						except Exception as error :
							logging.error(traceback.format_exc())
							raise error

			elif i[-3:] != '.py' or i == "__init__.py" or os.path.isdir("%s/%s"%(path, i)) :
				continue
			else:
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
	async def connect(config) :
		vendor = config["vendor"]
		if vendor == Vendor.POSTGRESQL :
			try :
				import asyncpg
			except :
				logging.warning("*** Warning asyncpg cannot be imported.")
			connection = await asyncpg.connect(
				user=config["user"],
				password=config["password"],
				host=config["host"],
				port=config["port"],
				database=config["database"]
			)
			return connection
		elif vendor == Vendor.MARIADB or vendor == Vendor.MYSQL :
			try :
				import aiomysql
			except :
				logging.warning("Module aiomysql cannot be imported.")
			connection = await aiomysql.connect(
				host=config['host'],
				port=config['port'],
				user=config['user'],
				password=config['password'],
				db=config["database"]
			)
			return connection
		elif vendor == Vendor.ORACLE :
			try :
				import cx_Oracle_async
			except :
				logging.warning("Module cx_Oracle_async cannot be imported.")

			pool = await cx_Oracle_async.create_pool(
				host=config['host'],
				port=config['port'],
				user=config['user'],
				password=config['password'],
				service_name=config['domain'],
			)
			connection = await pool.acquire()
			connection.autocommit = True
			return connection
		elif vendor == Vendor.SQLITE :
			try :
				import aiosqlite
			except :
				logging.warning("Module aiosqlite cannot be imported.")
			return await aiosqlite.connect(
				config["database"],
				isolation_level=None,
				check_same_thread=False
			)
		elif vendor == Vendor.MSSQL :
			try :
				import aioodbc
			except :
				logging.warning("Module aioodbc cannot be imported.")

			connection = await aioodbc.connect(dsn=f"""
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
	async def connectRoundRobin(config) :
		connector = AsyncRoundRobinConnector(config)
		vendor = config["vendor"]
		hasCursor =  vendor != Vendor.POSTGRESQL
		await connector.connect(hasCursor)
		return connector