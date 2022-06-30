#!/usr/bin/python3

from xerial.DBSessionPool import DBSessionPool

from Worker import Worker
from WorkerStructure import WorkerStructure

import json

class DBSessionTest :
	def __init__(self, config) :
		self.config = config
	
	def start(self) :
		self.pool = DBSessionPool(self.config)
		self.pool.createConnection()
		self.session = self.pool.getSession()
		self.session.appendModel(Worker)
		self.session.appendModel(WorkerStructure)
		self.session.createTable()
		
		structure = WorkerStructure()
		structure.division = "Stand User"
		structure.section = "Joestar"
		structure.line = "Speed and Strength"
		self.session.insert(structure)

		worker1 = Worker()
		worker1.structure = structure
		worker1.workerNo = '301-201-0001'
		worker1.firstName = 'Jonathan'
		worker1.lastName = 'Joestar'
		worker1.departmentID = 201
		worker1.companyID = 301
		worker1.salary = 35_000
		self.session.insert(worker1)
		workerList = self.session.select(Worker, "ORDER BY workerID", True, limit=10, offset=2)

		worker2 = Worker()
		worker2.structure = structure
		worker2.workerNo = '301-201-0002'
		worker2.firstName = 'Joseph'
		worker2.lastName = 'Joestar'
		worker2.departmentID = 201
		worker2.companyID = 301
		worker2.salary = 32_000
		self.session.insertMultiple([worker1, worker2])
		workerList = self.session.select(Worker, "ORDER BY workerID DESC", True, limit=10, offset=2)

		if len(workerList) >= 2 :
			self.session.drop(workerList[1])

		if len(workerList) >= 3 :
			self.session.dropByID(Worker, workerList[2].workerID)

		worker3 = workerList[0]
		worker3.firstName = "Jotaro"
		worker3.lastName = "Kujo"
		self.session.update(worker3)
		workerList = self.session.select(Worker, "WHERE workerID=%d"%(worker3.workerID), True)
		print([i.toDict() for i in workerList])

		print(">>> Count", self.session.count(Worker, ""))
		

if __name__ == '__main__' :
	with open('/etc/xerial/Xerial.json') as fd :
		config = json.load(fd)
	
	test = DBSessionTest(config)
	test.start()