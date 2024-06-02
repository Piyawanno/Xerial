from enum import IntEnum

class FilterOperation (IntEnum) :
	EQUAL = 10
	NOT_EQUAL = 11
	GREATER = 20
	GREATER_EQUAL = 21
	LESS = 30
	LESS_EQUAL = 31
	LIKE = 40
	IN = 50
	NOT_IN = 51
	BETWEEN = 60
	CONTAIN = 70
	NOT_CONTAIN = 71

FilterOperation.sign = {
	FilterOperation.EQUAL : '=',
	FilterOperation.NOT_EQUAL : '!=',
	FilterOperation.GREATER : '>',
	FilterOperation.GREATER_EQUAL : '>=',
	FilterOperation.LESS : '<',
	FilterOperation.LESS_EQUAL : '<=',
	FilterOperation.LIKE : 'LIKE',
	FilterOperation.IN : 'IN',
	FilterOperation.NOT_IN : 'NOT IN',
	FilterOperation.BETWEEN : 'BETWEEN',
	FilterOperation.CONTAIN : 'CONTAIN',
	FilterOperation.NOT_CONTAIN : 'NOT CONTAIN'
}