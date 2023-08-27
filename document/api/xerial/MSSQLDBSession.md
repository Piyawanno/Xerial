Module xerial.MSSQLDBSession
============================

Classes
-------

`MSSQLDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionBase.DBSessionBase

    ### Descendants

    * xerial.AsyncMSSQLDBSession.AsyncMSSQLDBSession

    ### Methods

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

    `generateCountQuery(self, modelClass, clause)`
    :

    `generateCreateTable(self, model)`
    :

    `generateIndexQuery(self, model)`
    :

    `generateInsert(self, modelClass, isAutoID=True)`
    :

    `generateRawSelectQuery(self, tableName, clause, limit=None, offset=None)`
    :

    `generateRawUpdateQuery(self, modelClass, raw)`
    :

    `generateResetID(self, modelClass: type) ‑> str`
    :

    `generateSelectQuery(self, modelClass, clause, limit=None, offset=None)`
    :

    `generateUpdateQuery(self, record)`
    :

    `getExistingTable(self)`
    :

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `prepareStatement(self, modelClass)`
    :

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :