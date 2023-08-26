Module xerial.Record
====================

Classes
-------

`Record(**kw)`
:   

    ### Static methods

    `checkBackup(modelClass)`
    :

    `checkPrimary(modelClass)`
    :

    `checkTableName(modelClass, prefix: str)`
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

    `setVendor(modelClass, vendor)`
    :

    ### Methods

    `copy(self, other)`
    :

    `createModification(self, version: str)`
    :

    `dereference(self)`
    :

    `fromDict(self, data: dict, isID: bool = False)`
    :

    `fromRawDict(self, data: dict)`
    :

    `initRelation(self, **kw)`
    :

    `modify(self)`
    :

    `setAsChildrenOf(self)`
    :

    `toDict(self) ‑> dict`
    :

    `toOption(self)`
    :

    `toRawDict(self) ‑> dict`
    :