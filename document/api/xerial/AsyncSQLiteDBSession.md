Module xerial.AsyncSQLiteDBSession
==================================

Classes
-------

`AsyncSQLiteDBSession(config)`
:   

    ### Ancestors (in MRO)

    * xerial.SQLiteDBSession.SQLiteDBSession
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

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `update(self, record)`
    :

    `updateDirect(self, modelClass, raw)`
    :