from typing import List

from packaging.version import Version

from xerial.Children import Children
from xerial.Column import Column
from xerial.DateColumn import DateColumn
from xerial.DateTimeColumn import DateTimeColumn
from xerial.FloatColumn import FloatColumn
from xerial.FractionColumn import FractionColumn
from xerial.IntegerColumn import IntegerColumn
from xerial.JSONColumn import JSONColumn
from xerial.ModificationType import ModificationType
from xerial.StringColumn import StringColumn
from xerial.Vendor import Vendor
from xerial.exception.ModificationException import ModificationException
from xerial.modact.ModificationAction import ModificationAction
from xerial.modact.ModificationActionFactory import ModificationActionFactory

StringColumn.compatible = {JSONColumn}
JSONColumn.compatible = {StringColumn}
DateColumn.compatible = {DateTimeColumn}
DateTimeColumn.compatible = {DateColumn}
IntegerColumn.compatible = {FloatColumn, FractionColumn}
FloatColumn.compatible = {IntegerColumn, FractionColumn}


def generateColumn(column, hasDefault=True):
	notNull = "NOT NULL" if column.isNotNull else ""
	if hasDefault:
		isDefault = hasattr(column, 'default') and column.default is not None
		defaultValue = column.default() if callable(column.default) else column.default
		default = "DEFAULT %s" % (column.setValueToDB(defaultValue)) if isDefault else ""
	else:
		default = ""
	return f"{column.getDBDataType()} {default} {notNull}"


__POSTGRESQL_GENERATOR__ = {
	ModificationType.ADD: lambda t, n, c: f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP: lambda t, n: f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME: lambda t, o, n: f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} TYPE {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} TYPE {generateColumn(c, False)}",
	ModificationType.ADD_INDEX: lambda t, n: f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX: lambda t, n: f"DROP INDEX IF EXISTS {t}_{n}",
}

__ORACLE_GENERATOR__ = {
	ModificationType.ADD: lambda t, n, c: f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP: lambda t, n: f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME: lambda t, o, n: f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX: lambda t, n: f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX: lambda t, n: f"DROP INDEX IF EXISTS {t}_{n}",
}

__MARIADB_GENERATOR__ = {
	ModificationType.ADD: lambda t, n, c: f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP: lambda t, n: f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME: lambda t, o, n: f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX: lambda t, n: f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX: lambda t, n: f"DROP INDEX IF EXISTS {t}_{n}",
}

__SQLITE_GENERATOR__ = {
	ModificationType.ADD: lambda t, n, c: f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP: lambda t, n: f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME: lambda t, o, n: f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX: lambda t, n: f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX: lambda t, n: f"DROP INDEX IF EXISTS {t}_{n}",
}

__MSSQL_GENERATOR__ = {
	ModificationType.ADD: lambda t, n, c: f"ALTER TABLE {t} ADD {n} {generateColumn(c)}",
	ModificationType.DROP: lambda t, n: f'ALTER TABLE {t} DROP COLUMN {n}',
	ModificationType.RENAME: lambda t, o, n: f'ALTER TABLE {t} RENAME COLUMN {o} TO {n}',
	ModificationType.CHANGE_TYPE: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c)}",
	ModificationType.CHANGE_LENGTH: lambda t, n, c: f"ALTER TABLE {t} ALTER COLUMN {n} {generateColumn(c, False)}",
	ModificationType.ADD_INDEX: lambda t, n: f"CREATE INDEX IF NOT EXISTS {t}_{n} ON {t}({n})",
	ModificationType.DROP_INDEX: lambda t, n: f"DROP INDEX IF EXISTS {t}_{n}",
}

__GENERATOR__ = {
	Vendor.POSTGRESQL: __POSTGRESQL_GENERATOR__,
	Vendor.MARIADB: __MARIADB_GENERATOR__,
	Vendor.MYSQL: __MARIADB_GENERATOR__,
	Vendor.ORACLE: __ORACLE_GENERATOR__,
	Vendor.SQLITE: __SQLITE_GENERATOR__,
	Vendor.MSSQL: __MSSQL_GENERATOR__,
}


class Modification:
	def __init__(self, version: str, table: str, meta: list, vendor: Vendor):
		self.version = Version(version)
		self.table = table
		self.meta = {k: v for k, v in meta}
		self.vendor = vendor
		self.column: List[ModificationAction] = []
		self.skipped: Dict[str, List[ModificationAction]] = {}
		self.generator = __GENERATOR__[vendor]
		self.schema = None
		self.reverseModification = {
			ModificationType.ADD: self.drop,
			ModificationType.DROP: self.add,
			ModificationType.RENAME: lambda old, new: self.rename(new, old),
			ModificationType.CHANGE_TYPE: lambda name, old, new: self.changeType(name, new, old),
			ModificationType.CHANGE_LENGTH: lambda name, _: self.changeLength(name, 0),
			ModificationType.ADD_INDEX: self.dropIndex,
			ModificationType.DROP_INDEX: self.addIndex
		}

	def setSchema(self, schema):
		if schema is not None and len(schema): self.schema = schema

	def resetSchema(self):
		self.schema = None

	def add(self, name: str, column: Column) -> str:
		"""
		Add a column into the existing Model.

		Parameters
		----------
		name: str  name of the added column
		column: Column attribute of the added column
		"""
		column.name = name
		column.vendor = self.vendor
		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.ADD,
			name,
			column
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def drop(self, name: str, column: Column = None) -> str:
		"""
		Drop a column from the existing Model.

		Parameters
		----------
		name: str  name of the column to drop
		"""
		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.DROP,
			name,
			column
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def rename(self, oldName: str, newName: str) -> str:
		"""
		Rename a column in the existing Model.

		Parameters
		----------
		oldName: str  name of the existing column
		newName: str  desired new name of the existing column
		"""
		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.RENAME,
			oldName,
			None,
			newName
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def changeType(self, name: str, oldColumn: Column, newColumn: Column) -> str:
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
		newColumn.name = name
		newColumn.vendor = self.vendor
		existingColumn = self.meta.get(name, oldColumn)
		if newColumn.__class__ != existingColumn.__class__ and newColumn.__class__ not in existingColumn.compatible:
			raise ValueError(
				f'Column {existingColumn.__class__.__name__} cannot be changed to {newColumn.__class__.__name__}.'
			)
		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.CHANGE_TYPE,
			name,
			oldColumn,
			newColumn
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def changeLength(self, name: str, length: int) -> str:
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
		existingColumn = self.meta.get(name, StringColumn(length=length))

		if not isinstance(existingColumn, StringColumn):
			raise ValueError(f'Column name {name} is not StringColumn. Length cannot be changed.')

		existingColumn.vendor = self.vendor
		if length > existingColumn.length:
			existingColumn.length = length

		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.CHANGE_LENGTH,
			name,
			existingColumn
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def addIndex(self, name: str) -> str:
		"""
		Add index to the given column in the existing Model.

		Parameters
		----------
		name: str  name of the column to add index
		"""
		if name not in self.meta:
			raise ValueError(f'Column name {name} does not exist and cannot be dropped.')
		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.ADD_INDEX,
			name,
			None
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def dropIndex(self, name: str) -> str:
		"""
		Drop index from the given column in the existing Model.

		Parameters
		----------
		name: str  name of the column to drop index
		"""
		if name not in self.meta:
			raise ValueError(f'Column name {name} does not exist and cannot be dropped.')
		modificationAction = ModificationActionFactory.create(
			self.table,
			self.version.__str__(),
			ModificationType.DROP_INDEX,
			name,
			None
		)
		self.column.append(modificationAction)
		return modificationAction.__str__()

	def generateQuery(self) -> List[str]:
		generated = []
		for action in self.column:
			if action.modificationType == ModificationType.DROP or isinstance(action.column, Children):
				continue
			if self.schema is not None:
				action.table = f'{self.schema}{action.table}'
			generated.append(self.generator[action.modificationType](*action.tuple()))

		return generated

	def reverse(self, modificationAction: ModificationAction) -> None:
		action = self.reverseModification.get(modificationAction.modificationType)
		if action is None:
			raise ValueError(f'Unknown modification type {modificationAction.modificationType}')

		action(*modificationAction.reverseArgs())

	def analyze(self) -> List[ModificationException]:
		exceptions = []
		for action in self.column:
			exceptions.extend(action.analyze())
		return exceptions

	def getSkippedActions(self) -> List[ModificationAction]:
		actions = []
		for version, action in self.skipped.items():
			actions.extend(action)
		return actions


	@staticmethod
	def generateAddQuery(vendor: Vendor, model: type, column: Column) -> str:
		generator = __GENERATOR__[vendor]
		return generator[ModificationType.ADD](model.__full_table_name__, column.name, column)
