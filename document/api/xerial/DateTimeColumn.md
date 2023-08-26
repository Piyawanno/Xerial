Module xerial.DateTimeColumn
============================

Classes
-------

`DateTimeColumn(isPrimary=False, length=0, isNotNull=False, default=None, foreignKey=None, isIndex=False, isRepresentative=False, input=None)`
:   

    ### Ancestors (in MRO)

    * xerial.Column.Column

    ### Class variables

    `compatible`
    :

    ### Static methods

    `getDayLater(dayNumber: int)`
    :

    `getDayLaterString(dayNumber: int)`
    :

    `getLater(seconds: int)`
    :

    `getLaterString(seconds: int)`
    :

    `getNow()`
    :

    `getNowString()`
    :

    ### Methods

    `fromDict(self, data)`
    :

    `getDBDataType(self)`
    :

    `parseValue(self, value)`
    :

    `setValueToDB(self, attribute)`
    :

    `toDict(self, attribute)`
    :