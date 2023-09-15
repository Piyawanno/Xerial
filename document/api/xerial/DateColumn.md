Module xerial.DateColumn
========================

Classes
-------

`DateColumn(isPrimary=False, length=0, isNotNull=False, default=None, foreignKey=None, isIndex=False, isRepresentative=False, parentModel: List[type] = [], input=None)`
:   

    ### Ancestors (in MRO)

    * xerial.Column.Column

    ### Class variables

    `compatible`
    :

    ### Static methods

    `getDayAfterToday(dayNumber: int)`
    :

    `getDayAfterTodayString(dayNumber: int)`
    :

    `getStartDate(data)`
    :

    `getToday()`
    :

    `getTodayString()`
    :

    `getYearAfterToday(yearNumber: int)`
    :

    `getYearAfterTodayString(yearNumber: int)`
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