from xerial.DBSessionBase import DBSessionBase

import logging

class DBExecutableSession (DBSessionBase) :
	def insert(self, record) :
		pass
	
	def insertMultiple(self, recordList) :
		pass
	
	def update(self, record) :
		pass
	
	def drop(self, record) :
		pass
	
	def dropByID(self, modelClass, id) :
		pass
	
	def createTable(self) :
		pass
	
	def getExistingTable(self) :
		pass

	def count(self, modelClass, clause) :
		query = self.generateCountQuery(modelClass, clause)
		cursor = self.executeRead(query)
		for i in cursor :
			return i[0]

	def select(self, modelClass, clause, isRelated=False, limit=None, offset=None, isDebug=False) :
		query = self.generateSelectQuery(modelClass, clause, limit, offset)
		cursor = self.executeRead(query)
		result = []
		for row in cursor :
			record = modelClass()
			i = 0
			for columnName, column in modelClass.meta :
				logging.debug(columnName, row[i])
				setattr(record, columnName, column.processValue(row[i]))
				i += 1
			result.append(record)
		if isRelated : self.selectRelated(modelClass, result)
		return result
	
	def selectRelated(self, modelClass, recordList) :
		if len(recordList) == 0 : return
		for attribute, table, primary in modelClass.foreignKey :
			keyList = [str(getattr(i, attribute)) for i in recordList]
			clause = "WHERE %s IN(%s)"%(primary, ",".join(keyList))
			related = self.select(self.model[table], clause, False)
			relatedMap = {getattr(i, primary):i for i in related}
			for record in recordList :
				value = getattr(record, attribute)
				setattr(record, attribute, relatedMap.get(value, value))