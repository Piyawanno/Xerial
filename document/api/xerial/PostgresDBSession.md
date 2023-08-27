Module xerial.PostgresDBSession
===============================

Classes
-------

`PostgresDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionBase.DBSessionBase

    ### Descendants

    * xerial.AsyncPostgresDBSession.AsyncPostgresDBSession

    ### Methods

    `closeConnection(self)`
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

    `dropByID(self, modelClass, ID)`
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

    `generateCountQuery(self, modelClass, clause)`
    :

    `generateCreateSchema(self, schema)`
    :

    `generateCreateTable(self, model)`
    :

    `generateDropTable(self, modelClass: type) ‑> str`
    :

    `generateIndexCheckQuery(self, model)`
    :

    `generateIndexQuery(self, model, columnName)`
    :

    `generateInsertMultipleQuery(self, modelClass, isAutoID=True)`
    :

    `generateInsertQuery(self, record, isAutoID=True)`
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

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `prepareStatement(self, modelClass)`
    :

    `processClause(self, clause: str, parameter: list) ‑> str`
    :

    `setSchema(self, schema)`
    :

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :