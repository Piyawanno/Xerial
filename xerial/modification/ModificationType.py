from enum import IntEnum

class ModificationType (IntEnum) :
	ADD = 1
	DROP = 2
	RENAME = 3
	CHANGE_TYPE = 4
	CHANGE_LENGTH = 5
	ADD_INDEX = 6
	DROP_INDEX = 7