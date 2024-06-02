from enum import IntEnum

from xerial.ColumnType import ColumnType
from xerial.ModificationType import ModificationType


class ExceptionCode(IntEnum):
	XERIAL = 0
	MODIFICATION = 1
	CHANGE_TYPE = int(f"{MODIFICATION}{ModificationType.CHANGE_TYPE}")
	DATETIME_TO_DATE = int(f"{CHANGE_TYPE}{ColumnType.DATE_TIME}{ColumnType.DATE}")
	TYPE_INCOMPATIBLE = int(f"{CHANGE_TYPE}0")
