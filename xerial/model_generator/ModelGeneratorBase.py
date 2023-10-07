#!/usr/bin/python3

import logging

__JS_CONSTRUCTOR__ = """
var {{Record}} = require('../orm/Record');
{importList}

class {modelName} extends Record{{
	constructor(){{
		super();
		if('__meta__' in this.constructor) return;
		this.__table_name__ = '{tableName}';
		this.__has_primary__ = {hasPrimary};

{attributeList}
	}}
}}

exports.{modelName} = {modelName};
"""

__PY_CONSTRUCTOR__ = """
from xerial.Record import Record
{importList}

class {modelName} (Record) :
	__table_name__ = '{tableName}'
	__has_primary__ = {hasPrimary}
	__is_increment__ = {isIncrement}

{attributeList}

"""

class ModelGeneratorBase :
	def __init__(self, config) :
		self.config = config
		self.outputPath = config["generator"]['outputPath']
		self.exception = {i.upper() for i in config["generator"]['exception']}
		self.isIncrement = config["generator"]["isIncrement"]
	
	def connect(self) :
		pass
	
	def getTableName(self) :
		return {}
	
	def getColumnName(self, tableName, owner) :
		return set()
	
	def getColumnInfo(self, tableName, owner) :
		return set()

	def getPrimaryColumn(self, tableName, owner) :
		return set()
	
	def getColumnClassName(self, columnType) :
		return 'IntegerColumn'
	
	def generatePythonColumn(self, raw, isPrimary) :
		return ""
	
	def generateJSColumn(self, raw, isPrimary) :
		return ""
		
	def generateJS(self) :
		self.getTableName()
		for tableName, owner in self.tableName :
			if tableName.upper() in self.exception : continue
			modelName = self.normalizeModelName(tableName)
			columnName = self.getColumnName(tableName, owner)
			columnInfo = self.getColumnInfo(tableName, owner)
			primaryColumn = self.getPrimaryColumn(tableName, owner)
			processed = [self.generateJSColumn(k, j in primaryColumn) for j, k in zip(columnName, columnInfo)]
			rendered, columnClass = zip(*processed)
			generated =	__JS_CONSTRUCTOR__.format(
				modelName=modelName,
				tableName=tableName,
				hasPrimary='true' if len(primaryColumn) else 'false',
				isIncrement='true' if self.isIncrement else 'false',
				importList="\n".join([f"var {{{i}}} = require('../orm/{i}');" for i in set(columnClass)]),
				attributeList="\n".join(rendered)
			)
			logging.info(tableName, modelName)
			with open(f"{self.outputPath}/{modelName}.js", "wt") as fd :
				fd.write(generated)
	
	def generatePython(self) :
		self.getTableName()
		for tableName, owner in self.tableName :
			if tableName not in {"R_REPORT_NAME"} : continue
			modelName = self.normalizeModelName(tableName)
			columnName = self.getColumnName(tableName, owner)
			columnInfo = self.getColumnInfo(tableName, owner)
			primaryColumn = self.getPrimaryColumn(tableName, owner)
			processed = [self.generatePythonColumn(k, j in primaryColumn) for j, k in zip(columnName, columnInfo)]
			rendered, columnClass = zip(*processed)
			generated =	__PY_CONSTRUCTOR__.format(
				modelName=modelName,
				tableName=tableName,
				hasPrimary='True' if len(primaryColumn) else 'False',
				isIncrement='True' if self.isIncrement else 'False',
				importList="\n".join([f"from xerial.{i} import {i}" for i in set(columnClass)]),
				attributeList="\n".join(rendered)
			)
			logging.info(tableName, modelName)
			with open(f"{self.outputPath}/{modelName}.py", "wt") as fd :
				fd.write(generated)
	
	def normalizeModelName(self, tableName) :
		wordList = tableName.split("_")
		if len(wordList[0]) == 1 : wordList = wordList[1:]
		normalizeWord = lambda x : x[0].upper() + x[1:].lower()
		return "".join([normalizeWord(i) for i in wordList])

	def renderOptionValue(self, value) :
		if isinstance(value, str) : return "'%s'"%(value)
		elif isinstance(value, bytes) : return str(value)
		elif isinstance(value, int) : return str(value)
		elif isinstance(value, float) : return str(value)
		elif isinstance(value, bool) : return str(value)
		else : raise ValueError