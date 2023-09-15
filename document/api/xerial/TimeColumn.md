Module xerial.TimeColumn
========================

Classes
-------

`TimeColumn(isPrimary=False, length=0, isNotNull=False, default=None, foreignKey=None, isIndex=False, isRepresentative=False, parentModel: List[type] = [], input=None)`
:   

    ### Ancestors (in MRO)

    * xerial.Column.Column

    ### Descendants

    * xerial.DayIntervalColumn.DayIntervalColumn

    ### Static methods

    `toSeconds(data)`
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