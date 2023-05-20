from xerial.Currency import Currency
from xerial.DateColumn import DATE_FORMAT
from fractions import Fraction
from datetime import datetime
from typing import Union

COMMON_CURRENCY_MAP = Currency.loadData()

class CurrencyData :
	origin: Fraction
	exchanged: Fraction
	originCurrency: Currency
	exchangedCurrency: Currency
	rate: Fraction
	exchangeDate: datetime

	def __init__(self, origin:Union[float, str]=0.0, currency:str="THB") :
		self.origin = Fraction(origin)
		self.originCurrency = COMMON_CURRENCY_MAP.get(currency, None)
		self.rate = Fraction("1.0")
		self.exchanged = None
		self.exchangedCurrency = None
		self.exchangeDate = None

	def __repr__(self) -> str:
		return f"{self.origin} {self.originCurrency}"

	def exchange(self, rate:Union[float, str], currency:str) :
		self.rate = Fraction(rate)
		self.exchanged = self.origin*self.rate
		self.exchangedCurrency = COMMON_CURRENCY_MAP.get(currency, None)
		self.exchangeDate = datetime.now()

	def fromDict(self, raw) :
		self.origin = Fraction(raw["originString"])
		exchanged = raw.get("exchangedString", None)
		self.exchanged = None if exchanged is None else Fraction(exchanged)
		self.originCurrency = COMMON_CURRENCY_MAP.get(raw.get("originCurrency", "THB"), None)
		exchangedCurrency = raw.get("exchangedCurrency", None)
		self.exchangedCurrency = None if exchangedCurrency  is None else COMMON_CURRENCY_MAP.get(exchangedCurrency, None)
		rate = raw.get("rateString", None)
		self.rate = None if rate is None else Fraction(rate)
		exchangeDate = raw.get("exchangeDate", None)
		self.exchangeDate = None if exchangeDate is None else datetime.strptime(exchangeDate, DATE_FORMAT)
		return self

	def toDict(self) :
		return {
			'origin' : [self.origin.numerator, self.origin.denominator],
			'originValue' : float(self.origin),
			'originString' : f"{self.origin.numerator}/{self.origin.denominator}",
			'originCurrency' : None if self.originCurrency is None else self.originCurrency.code,
			'exchanged' : None if self.exchanged is None else [self.exchanged.numerator, self.exchanged.denominator],
			'exchangedString' : None if self.exchanged is None else f"{self.exchanged.numerator}/{self.exchanged.denominator}",
			'exchangedValue' : None if self.exchanged is None else float(self.exchanged),
			'exchangedCurrency' : None if self.exchangedCurrency is None else self.exchangedCurrency.code,
			'rate' : None if self.rate is None else [self.rate.numerator, self.rate.denominator],
			'rateString' : None if self.rate is None else f"{self.rate.numerator}/{self.rate.denominator}",
			'rateValue' : None if self.rate is None else float(self.rate),
			'exchangeDate' : None if self.exchangeDate is None else self.exchangeDate.strftime(DATE_FORMAT)
		}