from enum import IntEnum

class FilterConjunction :
	AND = 1
	OR = 2

FilterConjunction.sign = {
	FilterConjunction.AND : 'AND',
	FilterConjunction.OR : 'OR',
}