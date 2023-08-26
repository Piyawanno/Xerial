Module xerial.DBExecutableSession
=================================

Classes
-------

`DBExecutableSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionBase.DBSessionBase

    ### Methods

    `count(self, modelClass, clause)`
    :

    `createTable(self)`
    :

    `drop(self, record)`
    :

    `dropByID(self, modelClass, id)`
    :

    `getExistingTable(self)`
    :

    `insert(self, record)`
    :

    `insertMultiple(self, recordList)`
    :

    `select(self, modelClass, clause, isRelated=False, limit=None, offset=None, isDebug=False)`
    :

    `selectRelated(self, modelClass, recordList)`
    :

    `update(self, record)`
    :