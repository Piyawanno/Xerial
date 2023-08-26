Module xerial.OracleDBSession
=============================

Classes
-------

`OracleDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionBase.DBSessionBase

    ### Descendants

    * xerial.AsyncOracleDBSession.AsyncOracleDBSession

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

    `generateCheckTable(self)`
    :

    `generateCountQuery(self, modelClass, clause)`
    :

    `generateCreatTable(self, model)`
    :

    `generateCreateIndex(self, model, columnName)`
    :

    `generateIndexQuery(self, model)`
    :

    `generateInsert(self, modelClass, isAutoID=True, isMultiple=False)`
    :

    `generateRawSelectQuery(self, tableName, clause, limit=None, offset=None)`
    :

    `generateRawUpdate(self, modelClass, raw)`
    :

    `generateResetID(self, modelClass: type) ‑> str`
    :

    `generateSelectQuery(self, modelClass, clause, limit=None, offset=None)`
    :

    `generateUpdate(self, record)`
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

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :