Module xerial.Record
====================

Classes
-------

`Record(**kw)`
:   

    ### Static methods

    `appendGroup(modelClass, label: str, value: int, order: str, inputPerLine: int = 2)`
    :

    `checkBackup(modelClass)`
    :

    `checkPrimary(modelClass)`
    :

    `checkTableName(modelClass, prefix: str)`
    :

    `disableInput(modelClass, columnName: str)`
    :

    `enableDefaultBackup()`
    :

    `extractAttribute(modelClass, primaryMeta)`
    :

    `extractChildren(modelClass)`
    :

    `extractGroupInput(modelClass, inputGroupMapper, groupedInputList: list = [])`
    :

    `extractInput(modelClass, extendedInput: List[xerial.Input.Input] = [])`
    :

    `extractMeta(modelClass)`
    :

    `hasMeta(modelClass)`
    :

    `hasParent(modelClass)`
    :

    `parseTime(delta)`
    :

    `replaceInput(modelClass, columnName: str, input: xerial.Input.Input)`
    :

    `setVendor(modelClass, vendor)`
    :

    ### Methods

    `copy(self, other)`
    :

    `createModification(self, version: str)`
    :   Create a Modification object to modify Structure of Model.
        
        Parameters
        ----------
        version: String of the new version of modification e.g. '2.0'.

    `dereference(self)`
    :

    `fromDict(self, data: dict, isID: bool = False)`
    :

    `fromRawDict(self, data: dict)`
    :

    `initRelation(self, **kw)`
    :

    `modify(self)`
    :   A placeholder method for Structure Modification. By calling
        DBSession.checkModification(), this method of each Model
        registered to the DBSession will be called. To implement
        Structure Modification, this method must be overridden
        by creating Modification object with the method
        Record.createModification()

    `setAsChildrenOf(self)`
    :

    `toDict(self) ‑> dict`
    :

    `toOption(self)`
    :

    `toRawDict(self) ‑> dict`
    :