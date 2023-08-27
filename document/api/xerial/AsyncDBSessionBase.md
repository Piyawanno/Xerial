Module xerial.AsyncDBSessionBase
================================

Classes
-------

`AsyncDBSessionBase(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionBase.DBSessionBase

    ### Descendants

    * xerial.AsyncMSSQLDBSession.AsyncMSSQLDBSession
    * xerial.AsyncMariaDBSession.AsyncMariaDBSession
    * xerial.AsyncOracleDBSession.AsyncOracleDBSession
    * xerial.AsyncPostgresDBSession.AsyncPostgresDBSession
    * xerial.AsyncSQLiteDBSession.AsyncSQLiteDBSession

    ### Methods

    `checkModelModification(self, modelClass, currentVersion)`
    :

    `closeConnection(self)`
    :

    `connect(self, connection=None)`
    :

    `convertRaw(self, fetched)`
    :

    `count(self, modelClass: type, clause: str, parameter: list = None) ‑> int`
    :

    `createConnection(self)`
    :

    `createTable(self)`
    :

    `drop(self, record)`
    :

    `dropByCondition(self, modelClass, condition)`
    :

    `dropByID(self, modelClass, id)`
    :

    `dropChildren(self, record, modelClass)`
    :

    `dropChildrenByID(self, recordID, modelClass)`
    :

    `executeRead(self, query, parameter=None)`
    :

    `executeWrite(self, query, parameter=None)`
    :

    `getExistingTable(self)`
    :

    `insertChildren(self, record, modelClass, isReturningID=True)`
    :

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `resetIDSequence(self, modelClass: type, renewStartID: int)`
    :

    `selectByID(self, modelClass: type, ID: int, isRelated: bool = False, isChildren: bool = False) ‑> xerial.Record.Record`
    :

    `selectCSV(self, descriptor, modelClass: type, clause: str, limit: int, offset: int, parameter: list = None)`
    :

    `selectChildren(self, modelClass, recordList)`
    :

    `selectExcel(self, fileName: str, modelClass: type, clause: str, limit: int = None, offset: int = None, parameter: list = None)`
    :

    `selectRaw(self, modelClass: type, clause: str, limit: int = None, offset: int = None, parameter: list = None) ‑> dict`
    :

    `selectRelated(self, modelClass, recordList)`
    :

    `selectTranspose(self, modelClass: type, clause: str, isRelated: bool = False, isChildren: bool = False, limit: int = None, offset: int = None, parameter: list = None) ‑> dict`
    :

    `setFieldByID(self, modelClass: type, fieldMap: Dict[str, Any], id: int)`
    :

    `setFieldByIDList(self, modelClass: type, fieldMap: Dict[str, Any], ids: List[int])`
    :

    `update(self, record)`
    :

    `updateChildren(self, record, modelClass)`
    :

    `updateDirect(self, modelClass, raw)`
    :