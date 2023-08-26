from xerial.Column import Column
from xerial.ModificationType import ModificationType
from xerial.StringColumn import StringColumn
from xerial.JSONColumn import JSONColumn
from xerial.DateColumn import DateColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.FloatColumn import FloatColumn
from xerial.FractionColumn import FractionColumn
from xerial.Children import Children
from xerial.Vendor import Vendor
from typing import List
from packaging.version import Version

StringColumn.compatible = {JSONColumn}
JSONColumn.compatible = {StringColumn}
DateColumn.compatible = {DateTimeColumn}
DateTimeColumn.compatible = {DateColumn}
IntegerColumn.compatible = {FloatColumn, FractionColumn}
FloatColumn.compatible = {IntegerColumn, FractionColumn}

def generateColumn(column, hasDefault=True) :
	notNull = "NOT NULL" if column.isNotNull else ""
	if hasDefault :
		isDefault = hasattr(column, 'default') and column.default is not None
		defaultValue = column.default() if callable(column.default) else column.default
		default = "DEFAULT %s"%(column.setValueToDB(defaultValue)) if isDefault else ""
	else :
		default = ""
	return f"{column.getDBDataType()} {default} {notNull}"

__POSTGRESQL_GERNARATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}', 
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} TYPE {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} TYPE {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__ORACLE_GERNARATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}', 
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__MARIADB_GERNARATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}', 
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__SQLITE_GERNARATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}', 
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__MSSQL_GERNARATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}', 
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__GENERATOR__ = {
	Vendor.POSTGRESQL : __POSTGRESQL_GERNARATOR__,
	Vendor.MARIADB : __MARIADB_GERNARATOR__,
	Vendor.MYSQL : __MARIADB_GERNARATOR__,
	Vendor.ORACLE : __ORACLE_GERNARATOR__,
	Vendor.SQLITE : __SQLITE_GERNARATOR__,
	Vendor.MSSQL : __MSSQL_GERNARATOR__,
}

class Modification :
	def __init__(self, version:str, table:str, meta:list, vendor:Vendor) :
		self.version = Version(version)
		self.table = table
		self.meta = {k:v for k, v in meta}
		self.vendor = vendor
		self.column = []
		self.generator = __GENERATOR__[vendor]
	
	def add(self, name:str, column:Column) :
		"""
		Add a column into the existing Model.
		
		Parameters
		----------
		name: str  name of the added column
		column: Column attribute of the added column
		"""
		column.name = name
		column.vendor = self.vendor
		self.column.append((ModificationType.ADD, self.table, name, column))
	
	def drop(self, name:str) :
		self.column.append((ModificationType.DROP, self.table, name))
	
	def rename(self, oldName:str, newName:str) :
		self.column.append((ModificationType.RENAME, self.table, oldName, newName))
	
	def changeType(self, name:str, column:Column) :
		column.name = name
		column.vendor = self.vendor
		existingColumn = self.meta.get(name, None)
		if existingColumn is None :
			raise ValueError(f'Column name {name} does not exist. Type cannot be changed.')
		if column.__class__ != existingColumn.__class__ and column.__class__ not in existingColumn.compatible :
			raise ValueError(f'Column {existingColumn.__class__.__name__} cannot be changed to {column.__class__.__name__}.')
		self.column.append((ModificationType.CHANGE_TYPE, self.table, name, column))
	
	def changeLength(self, name:str, length:int) :
		existingColumn = self.meta.get(name, None)
		if existingColumn is None :
			raise ValueError(f'Column name {name} does not exist. Length cannot be changed.')
		if not isinstance(existingColumn, StringColumn) :
			raise ValueError(f'Column name {name} is not StringColumn. Length cannot be changed.')
		existingColumn.length = length
		existingColumn.vendor = self.vendor
		self.column.append((ModificationType.CHANGE_LENGTH, self.table, name, existingColumn))
	
	def addIndex(self, name:str) :
		if name not in self.meta :
			raise ValueError(f'Column name {name} does not exist and cannot be dropped.')
		self.column.append((ModificationType.ADD_INDEX, self.table, name))
	
	def dropIndex(self, name:str) :
		if name not in self.meta :
			raise ValueError(f'Column name {name} does not exist and cannot be dropped.')
		self.column.append((ModificationType.DROP_INDEX, name))
	
	def generateQuery(self) -> List[str] :
		generated = []
		for column in self.column :
			if len(column) > 3 and isinstance(column[3], Children) : continue
			generated.append(self.generator[column[0]](*column[1:]))
		return generated
