Module xerial.SQLiteDBSession
=============================

Classes
-------

`SQLiteDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionBase.DBSessionBase

    ### Descendants

    * xerial.AsyncSQLiteDBSession.AsyncSQLiteDBSession

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

    `generateCountQuery(self, modelClass, clause)`
    :

    `generateCreateTable(self, model)`
    :

    `generateIndexCheckQuery(self, model)`
    :

    `generateIndexQuery(self, model, columnName)`
    :

    `generateInsertQuery(self, modelClass, isAutoID=True)`
    :

    `generateRawSelectQuery(self, tableName, clause, limit=None, offset=None)`
    :

    `generateRawUpdateQuery(self, modelClass, raw)`
    :

    `generateResetID(self, modelClass: type) ‑> str`
    :

    `generateSelectQuery(self, modelClass, clause, limit=None, offset=None)`
    :

    `generateTableQuery(self)`
    :

    `generateUpdateQuery(self, record)`
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

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :