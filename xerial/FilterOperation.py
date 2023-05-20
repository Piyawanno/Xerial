from enum import IntEnum

class FilterOperation (IntEnum) :
	EQUAL = 10
	NOT_EQUAL = 11
	GREATER = 20
	GREATER_EQUAL = 21
	LESS = 30
	LESS_EQUAL = 31
	LIKE = 40
	IN = 41

FilterOperation.sign = {
	FilterOperation.EQUAL : '=',
	FilterOperation.NOT_EQUAL : '!=',
	FilterOperation.GREATER : '>',
	FilterOperation.GREATER_EQUAL : '>=',
	FilterOperation.LESS : '<',
	FilterOperation.LESS_EQUAL : '<=',
	FilterOperation.LIKE : 'LIKE',
	FilterOperation.IN : 'IN',
}