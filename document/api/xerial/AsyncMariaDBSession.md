Module xerial.AsyncMariaDBSession
=================================

Classes
-------

`AsyncMariaDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.MariaDBSession.MariaDBSession
    * xerial.AsyncDBSessionBase.AsyncDBSessionBase
    * xerial.DBSessionBase.DBSessionBase

    ### Methods

    `closeConnection(self)`
    :

    `createConnection(self)`
    :

    `createIndex(self, model)`
    :

    `createTable(self)`
    :

    `drop(self, record)`
    :

    `dropByCondition(self, modelClass, clause)`
    :

    `dropByID(self, modelClass, ID)`
    :

    `executeRegularRead(self, query, parameter=None)`
    :

    `executeRegularWrite(self, query, parameter=None)`
    :

    `executeRoundRobinRead(self, query, parameter=None)`
    :

    `executeRoundRobinWrite(self, query, parameter=None)`
    :

    `getExistingTable(self)`
    :

    `insert(self, record, isAutoID=True)`
    :

    `insertMultiple(self, recordList, isAutoID=True, isReturningID=False)`
    :

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `prepareStatement(self, modelClass)`
    :

    `processClause(self, clause: str, parameter: list) ‑> str`
    :

    `selectRaw(self, query: str) ‑> List[Dict[str, Any]]`
    :

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :