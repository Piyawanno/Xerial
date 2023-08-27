Module xerial.AsyncPostgresDBSession
====================================

Classes
-------

`AsyncPostgresDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.PostgresDBSession.PostgresDBSession
    * xerial.AsyncDBSessionBase.AsyncDBSessionBase
    * xerial.DBSessionBase.DBSessionBase

    ### Methods

    `closeConnection(self)`
    :

    `connect(self, connection=None)`
    :

    `createConnection(self)`
    :

    `createIndex(self, model)`
    :

    `createSchema(self, schema)`
    :

    `createTable(self)`
    :

    `drop(self, record)`
    :

    `dropByCondition(self, modelClass, clause)`
    :

    `dropByID(self, modelClass, id)`
    :

    `dropChildren(self, record, modelClass)`
    :

    `dropChildrenByID(self, recordID, modelClass)`
    :

    `executeRegularRead(self, query, parameter=None)`
    :

    `executeRegularWrite(self, query, parameter=None)`
    :

    `executeRoundRobinRead(self, query, parameter=None)`
    :

    `executeRoundRobinWrite(self, query, parameter=None)`
    :

    `generateInsertMultipleQuery(self, modelClass, n: int, isAutoID=True)`
    :

    `getExistingTable(self)`
    :

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `insertMultipleWithID(self, modelClass: type, recordList: list, valueList: list)`
    :

    `prepareStatement(self, modelClass)`
    :

    `processClause(self, clause: str, parameter: list) ‑> str`
    :

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :