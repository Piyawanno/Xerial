#!/usr/bin/python3

from xerial.ModelGeneratorBase import ModelGeneratorBase

import cx_Oracle, json

__COLUMN_MAP__ = {
	"DB_TYPE_NVARCHAR" : "StringColumn",
	"DB_TYPE_VARCHAR" : "StringColumn",
	"DB_TYPE_CHAR" : "StringColumn",
	"DB_TYPE_CLOB" : "StringColumn",
	"DB_TYPE_NCLOB" : "StringColumn",
	"DB_TYPE_TIMESTAMP" : "DateTimeColumn",
	"DB_TYPE_DATE" : "DateColumn",
	"DB_TYPE_INTERVAL_DS" : "DayIntervalColumn",
}

class OracleModelGenerator (ModelGeneratorBase) :
	def connect(self) :
		user = self.config['user']
		password = self.config['password']
		host = self.config['host']
		port = self.config['port']
		domain = self.config['domain']
		connectionString = f'{user}/{password}@{host}:{port}/{domain}'
		self.connection = cx_Oracle.connect(connectionString)
		self.cursor = self.connection.cursor()
	
	def getTableName(self) :
		ownerList = self.config['owner']
		self.tableName = set()
		for owner in ownerList :
			query = f"SELECT table_name, owner  from all_tables WHERE owner='{owner}'"
			result = self.cursor.execute(query)
			self.tableName = self.tableName.union({(i[0], owner) for i in result})
		return self.tableName
	
	def getColumnName(self, tableName, owner) :
		query = f"SELECT * FROM {owner}.{tableName} OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY"
		self.cursor.execute(query)
		return [i[0].upper() for i in self.cursor.description]
	
	def getColumnInfo(self, tableName, owner) :
		return self.cursor.description
	
	def generateJSColumn(self, raw, isPrimary) :
		name = raw[0]
		type = raw[1].name
		length = raw[3]
		floatingPrecision = raw[5]
		option = {}
		if isPrimary :
			option['isPrimary'] = True
		if type == "DB_TYPE_NUMBER" :
			option['length'] = raw[4]
			if floatingPrecision <= 0 :
				columnType = "IntegerColumn"
			else :
				option['precision'] = raw[5]
				columnType = "FloatColumn"
		else :
			columnType = self.getColumnClassName(type)
		if columnType is None :
			raise TypeError("%s is not compatible."%(type))
		if length is not None :
			option["length"] = length
		if type == "DB_TYPE_CLOB" or type == "DB_TYPE_NCLOB" :
			option["length"] = -1
		renderedOption = json.dumps(option)
		return f"\t\tthis.{name} = new {columnType}({renderedOption});", columnType
	
	def generatePythonColumn(self, raw, isPrimary) :
		name = raw[0]
		type = raw[1].name
		length = raw[3]
		floatingPrecision = raw[5]
		option = {}
		if isPrimary :
			option['isPrimary'] = True
		if type == "DB_TYPE_NUMBER" :
			option['length'] = raw[4]
			if floatingPrecision <= 0 :
				columnType = "IntegerColumn"
			else :
				option['precision'] = raw[5]
				columnType = "FloatColumn"
		else :
			columnType = self.getColumnClassName(type)
		if columnType is None :
			raise TypeError("%s is not compatible."%(type))
		if length is not None :
			option["length"] = length
		if type == "DB_TYPE_CLOB" or type == "DB_TYPE_NCLOB" :
			option["length"] = -1
		renderedOption = ", ".join(["%s=%s"%(k, self.renderOptionValue(v)) for k, v in option.items()])
		return f"\t{name} = {columnType}({renderedOption})", columnType

	def getPrimaryColumn(self, tableName, owner) :
		query = f"""SELECT column_name FROM all_cons_columns WHERE constraint_name IN (
			SELECT constraint_name FROM all_constraints 
			WHERE UPPER(table_name) = '{tableName}' AND CONSTRAINT_TYPE = 'P'
		)"""
		result = self.cursor.execute(query)
		return [i[0] for i in result]
	
	def getColumnClassName(self, columnType) :
		return __COLUMN_MAP__.get(columnType, None)
