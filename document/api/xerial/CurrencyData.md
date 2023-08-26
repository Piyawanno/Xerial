Module xerial.CurrencyData
==========================

Classes
-------

`CurrencyData(origin: Union[float, str, fractions.Fraction] = 0.0, currency: str = 'THB')`
:   

    ### Class variables

    `exchangeDate: datetime.datetime`
    :

    `exchanged: fractions.Fraction`
    :

    `exchangedCurrency: xerial.Currency.Currency`
    :

    `origin: fractions.Fraction`
    :

    `originCurrency: xerial.Currency.Currency`
    :

    `rate: fractions.Fraction`
    :

    ### Methods

    `exchange(self, rate: Union[float, str], currency: str)`
    :

    `fromDict(self, raw)`
    :

    `toDict(self)`
    :