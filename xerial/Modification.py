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

from xerial.exception.FloatToIntException import FloatToIntException
from xerial.exception.ModificationException import ModificationException
from xerial.exception.TypeIncompatibleException import TypeIncompatibleException

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

__POSTGRESQL_GENERATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} TYPE {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} TYPE {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__ORACLE_GENERATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__MARIADB_GENERATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__SQLITE_GENERATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__MSSQL_GENERATOR__ = {
	ModificationType.ADD : lambda t, n, c : f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP : lambda t, n : f'',
	ModificationType.RENAME : lambda t, o, n : f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH : lambda t, n, c : f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX : lambda t, n : f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX : lambda t, n : f"DROP INDEX IF EXISTS {t}_{n}",
}

__GENERATOR__ = {
	Vendor.POSTGRESQL : __POSTGRESQL_GENERATOR__,
	Vendor.MARIADB : __MARIADB_GENERATOR__,
	Vendor.MYSQL : __MARIADB_GENERATOR__,
	Vendor.ORACLE : __ORACLE_GENERATOR__,
	Vendor.SQLITE : __SQLITE_GENERATOR__,
	Vendor.MSSQL : __MSSQL_GENERATOR__,
}

class Modification :
	def __init__(self, version:str, table:str, meta:list, vendor:Vendor) :
		self.version = Version(version)
		self.table = table
		self.meta = {k:v for k, v in meta}
		self.vendor = vendor
		self.column = []
		self.generator = __GENERATOR__[vendor]
		self.schema = None

	def setSchema(self, schema):
		if schema is not None and len(schema): self.schema = schema

	def resetSchema(self):
		self.schema = None

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

	def drop(self, name:str, column:Column=None) :
		"""
		Drop a column from the existing Model.

		Parameters
		----------
		name: str  name of the column to drop
		"""
		self.column.append((ModificationType.DROP, self.table, name, column))

	def rename(self, oldName:str, newName:str) :
		"""
		Rename a column in the existing Model.

		Parameters
		----------
		oldName: str  name of the existing column
		newName: str  desired new name of the existing column
		"""
		self.column.append((ModificationType.RENAME, self.table, oldName, newName))

	def changeType(self, name:str, column:Column) :
		"""
		Change type of the given column in the existing Model.

		NOTE 1) Type cannot be arbitrary changed.
		Xerial will check the compatibility between the existing type
		and the given type.

		NOTE 2) For change length of StringColumn from l<256 to l=-1,
		it means that the type of column will be changed.
		Instead of calling changeLength(), changeType will be called.

		Parameters
		----------
		name: str  name of the column to change type
		column: Column attribute of the column to change
		"""
		column.name = name
		column.vendor = self.vendor
		existingColumn = self.meta.get(name, None)
		if existingColumn is None :
			raise ValueError(f'Column name {name} does not exist. Type cannot be changed.')
		if column.__class__ != existingColumn.__class__ and column.__class__ not in existingColumn.compatible :
			raise ValueError(f'Column {existingColumn.__class__.__name__} cannot be changed to {column.__class__.__name__}.')
		self.column.append((ModificationType.CHANGE_TYPE, self.table, name, column))

	def changeLength(self, name:str, length:int) :
		"""
		Change length of the given StringColumn in the existing Model.

		NOTE 1) This method is only allowed for StringColumn.

		NOTE 2) For change length of StringColumn from l<256 to l=-1,
		it means that the type of column will be changed.
		Instead of calling changeLength(), changeType will be called.

		Parameters
		----------
		name: str  name of the column to change type
		length: int new length of the StringColumn to change
		"""
		existingColumn = self.meta.get(name, None)
		if existingColumn is None :
			raise ValueError(f'Column name {name} does not exist. Length cannot be changed.')
		if not isinstance(existingColumn, StringColumn) :
			raise ValueError(f'Column name {name} is not StringColumn. Length cannot be changed.')
		existingColumn.length = length if length > existingColumn.length else existingColumn.length
		existingColumn.vendor = self.vendor
		self.column.append((ModificationType.CHANGE_LENGTH, self.table, name, existingColumn))

	def addIndex(self, name:str) :
		"""
		Add index to the given column in the existing Model.

		Parameters
		----------
		name: str  name of the column to add index
		"""
		if name not in self.meta :
			raise ValueError(f'Column name {name} does not exist and cannot be dropped.')
		self.column.append((ModificationType.ADD_INDEX, self.table, name))

	def dropIndex(self, name:str) :
		"""
		Drop index from the given column in the existing Model.

		Parameters
		----------
		name: str  name of the column to drop index
		"""
		if name not in self.meta :
			raise ValueError(f'Column name {name} does not exist and cannot be dropped.')
		self.column.append((ModificationType.DROP_INDEX, self.table, name))

	def generateQuery(self) -> List[str] :
		generated = []
		for column in self.column :
			if len(column) > 3 and isinstance(column[3], Children) : continue
			if self.schema is not None :
				parameter = list(column)
				parameter[1] = f'{self.schema}{self.table}'
				generated.append(self.generator[parameter[0]](*parameter[1:]))
			else :
				generated.append(self.generator[column[0]](*column[1:]))
		return generated

	def reverse(self, t: tuple) -> None:
		reverse_modification = {
			ModificationType.ADD: self.drop,
			ModificationType.DROP: self.add,
			ModificationType.RENAME: lambda old, new: self.rename(new, old),
			ModificationType.CHANGE_TYPE: self.changeType,
			ModificationType.CHANGE_LENGTH: lambda name, _: self.changeLength(name, 0),
			ModificationType.ADD_INDEX: self.dropIndex,
			ModificationType.DROP_INDEX: self.addIndex
		}

		modification = reverse_modification.get(t[0])
		if modification is None:
			raise ValueError(f'Unknown modification type {t[0]}')

		modification(*t[2:])

	@staticmethod
	def analyze(self, modification: tuple) -> None:
		if modification[0] == ModificationType.CHANGE_TYPE:
			name = modification[2]
			new_column = modification[3].__class__
			existing_column = self.meta.get(name, None)

			if new_column not in existing_column.compatible:
				raise TypeIncompatibleException(name, existing_column.__class__.__name__, new_column.__name__)

			if new_column == IntegerColumn and existing_column.__class__ == FloatColumn:
				raise FloatToIntException(name)

		return None
