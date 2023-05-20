from xerial.PrimitiveStructure import PrimitiveStructure
from xerial.ForeignKey import ForeignKey
from xerial.StringColumn import StringColumn

from xlsxwriter import Workbook

from typing import Dict

class ExcelWriter :
	def __init__(self, modelClass, workbook:Workbook) :
		self.modelClass = modelClass
		if not hasattr(modelClass, 'primitive') :
			modelClass.primitive = PrimitiveStructure(modelClass)
		self.primitive = modelClass.primitive
		self.workbook = workbook
		self.worksheet = workbook.add_worksheet(modelClass.__name__)
		self.foreignKeyRow = {}
	
	def writeMain(self, cursor) :
		self.processForeign()
		self.writeColumnName()
		self.writeMainSheet(cursor)
	
	def getForeignClause(self, foreignKey:ForeignKey) -> str :
		index = self.primitive.foreignIndex[foreignKey.name]
		foreignKeyData = self.foreignSet[index]
		if isinstance(foreignKey.columnMeta, StringColumn) :
			keyList = {f"'{i}'" for i in foreignKeyData}
		else :
			keyList = {str(i) for i in foreignKeyData}
		return f"WHERE {foreignKey.column} IN({','.join(list(keyList))})"
	
	def writeForeign(self, foreignKey:ForeignKey, cursor) :
		sheet = self.foreignSheet[foreignKey.name]
		self.writeForeignColumnName(foreignKey, sheet)
		self.writeForeignSheet(cursor, foreignKey, sheet)
	
	def writeReference(self) :
		rowNumber = 1
		for referenceRow in self.referenceList :
			for j, referenceID in referenceRow.items() :
				foreignKey = self.primitive.foreignIndexMapper[j]
				sheetName = foreignKey.model.__name__
				referencedRow, label = self.foreignKeyRow[j][referenceID]
				self.worksheet.write_url(rowNumber, j, f"internal:'{sheetName}'!A{referencedRow}", string=label)
			rowNumber += 1
	
	def writeColumnName(self) :
		for i, (columnName, column) in enumerate(self.modelClass.meta) :
			self.worksheet.write(0, i, columnName)
	
	def writeForeignColumnName(self, foreignKey:ForeignKey, sheet) :
		for i, (columnName, column) in enumerate(foreignKey.model.meta) :
			sheet.write(0, i, columnName)
	
	def writeMainSheet(self, cursor) :
		rowNumber = 0
		self.referenceList = []
		for i, row in enumerate(cursor) :
			rowNumber = i+1
			for j, cell in enumerate(row) :
				self.worksheet.write(rowNumber, j, cell)
			for j, label in self.primitive.enumLabel :
				self.worksheet.write(rowNumber, j, label.get(row[j], row[j]))
			referenceRow = {}
			self.referenceList.append(referenceRow)
			for j in self.foreignSet.keys() :
				self.foreignSet[j].add(row[j])
				referenceRow[j] = row[j]
	
	def writeForeignSheet(self, cursor, foreignKey:ForeignKey, sheet) :
		rowNumber = 1
		index = self.primitive.foreignIndex[foreignKey.name]
		self.foreignKeyRow[index] = {}
		for i, row in enumerate(cursor) :
			rowNumber = i+1
			if foreignKey.representativeColumn == -1 :
				label = str(f"{foreignKey.modelName}:{row[0]}")
			for j, cell in enumerate(row) :
				sheet.write(rowNumber, j, cell)
				if j == foreignKey.representativeColumn : label = str(cell)
			self.foreignKeyRow[index][row[0]] = (rowNumber+1, label)
			for j, labelMap in foreignKey.enumLabel :
				sheet.write(rowNumber, j, labelMap.get(row[j], row[j]))
	
	def processForeign(self) :
		self.foreignSheet = {}
		self.foreignSet:Dict[int, set] = {}
		for foreignKey in self.modelClass.foreignKey :
			index = self.primitive.columnNameIndex[foreignKey.name]
			self.foreignSheet[foreignKey.name] = self.workbook.add_worksheet(foreignKey.modelName)
			self.foreignSet[index] = set()