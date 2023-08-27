Module xerial.DBSessionBase
===========================

Classes
-------

`DBSessionBase(config)`
:   

    ### Descendants

    * xerial.AsyncDBSessionBase.AsyncDBSessionBase
    * xerial.DBExecutableSession.DBExecutableSession
    * xerial.MSSQLDBSession.MSSQLDBSession
    * xerial.MariaDBSession.MariaDBSession
    * xerial.OracleDBSession.OracleDBSession
    * xerial.PostgresDBSession.PostgresDBSession
    * xerial.SQLiteDBSession.SQLiteDBSession

    ### Methods

    `appendModel(self, modelClass)`
    :

    `checkChildren(self, modelClass)`
    :

    `checkForeignKey(self, modelClass)`
    :

    `checkLinkingMeta(self, modelClass)`
    :

    `checkModelLinking(self)`
    :

    `checkModelModification(self, modelClass, currentVersion)`
    :

    `checkModification(self, versionPath: str)`
    :   Automatic checking of Structure Modification.
        
        Parameters
        ----------
        versionPath : Path to JSON file storing the current version
        of each model.

    `closeConnection(self)`
    :

    `connect(self, connection=None)`
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

    `dropTable(self, modelClass: type)`
    :

    `executeRead(self, query, parameter=None)`
    :

    `executeWrite(self, query, parameter=None)`
    :

    `generateDropCommand(self)`
    :

    `generateDropTable(self, modelClass: type) ‑> str`
    :

    `generateModification(self, modelClass, currentVersion)`
    :

    `generateRawSelectQuery(self, tableName, clause, limit=None, offset=None)`
    :

    `generateResetID(self, modelClass: type) ‑> str`
    :

    `generateSelectQuery(self, modelClass: type, clause: str, limit: int, offset: int) ‑> str`
    :

    `generateSetField(self, modelClass: type, fieldMap: Dict[str, Any], id: int) ‑> Tuple[str, list]`
    :

    `generateSetFieldIDList(self, modelClass: type, fieldMap: Dict[str, Any], ids: List[int]) ‑> Tuple[str, list]`
    :

    `getExistingTable(self) ‑> List[str]`
    :

    `getParent(self, modelClass)`
    :

    `getPrimaryClause(self, record)`
    :

    `getRawPrimaryClause(self, modelClass, raw)`
    :

    `getRawValue(self, record, isAutoID=True)`
    :

    `getValue(self, record, isAutoID=True)`
    :

    `insert(self, record, isAutoID=True)`
    :   Insert record into database.
        
        Parameters
        ----------
        record: Object of class Record or its inheritance to insert into database.
        
        isAutoID: If setting to True, primary key of the record will be
        auto generated from database. Otherwise, the primary key must be set.

    `insertChildren(self, record, modelClass)`
    :

    `insertMultiple(self, recordList, isAutoID=True, isReturningID=False)`
    :   Insert list of records into database.
        
        Parameters
        ----------
        recordList: List of Object of class Record or its inheritance to insert into database.
        
        isAutoID: If setting to True, primary key of the record will be
        auto generated from database. Otherwise, the primary key must be set.
        
        isReturningID: If setting to False and isAutoID=True,
        Although the primary key of the record will be auto generated,
        it will not set to the record due to the performance reason.

    `insertMultipleDirect(self, modelClass, rawList)`
    :

    `mapExecute(self)`
    :

    `prepareStatement(self, modelClass)`
    :

    `processClause(self, clause: str, parameter: list) ‑> str`
    :

    `resetCount(self)`
    :

    `resetIDSequence(self, modelClass: type, renewStartID: int)`
    :

    `select(self, modelClass: type, clause: str, isRelated: bool = False, isChildren: bool = False, limit: int = None, offset: int = None, parameter: list = None) ‑> list`
    :   Select data from database.
        
        Parameters
        ----------
        modelClass: Class of model to select
        
        clause: String of query clause, Xerial allows WHERE, ORDER BY, GROUP BY
        
        isRelated: By setting to True, the related data with foreignKey
        will be selected. Otherwise, the foreignKey column will have
        the reference value.
        
        isChildren: By setting to True, the children records will be selected.
        
        limit: Maximum number of records to select. If setting to None=no limit.
        
        offset: Offset of records to select. If setting to None=no offset.
        
        parameter: List of query parameter for the '?' placement
        in the clause parameter.

    `selectByID(self, modelClass: type, ID: int, isRelated: bool = False, isChildren: bool = False) ‑> xerial.Record.Record`
    :

    `selectCSV(self, descriptor, modelClass: type, clause: str, limit: int = None, offset: int = None, parameter: list = None)`
    :

    `selectChildren(self, modelClass, recordList)`
    :

    `selectExcel(self, fileName: str, modelClass: type, clause: str, limit: int = None, offset: int = None, parameter: list = None)`
    :

    `selectRaw(self, modelClass: type, clause: str, limit: int = None, offset: int = None, parameter: list = None) ‑> dict`
    :

    `selectRelated(self, modelClass, recordList)`
    :

    `selectTranspose(self, modelClass: type, clause: str, isRelated: bool = False, limit: int = None, offset: int = None, parameter: list = None) ‑> dict`
    :

    `setFieldByID(self, modelClass: type, fieldMap: Dict[str, Any], id: int)`
    :

    `setFieldByIDList(self, modelClass: type, fieldMap: Dict[str, Any], ids: List[int])`
    :

    `toTuple(self, modelClass, raw)`
    :

    `update(self, record)`
    :

    `updateChildren(self, record, modelClass)`
    :

    `updateDirect(self, modelClass, raw)`
    :

`PrimaryDataError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException