Module xerial.DBMigration
=========================

Functions
---------

    
`nullTransfer(raw: List[Dict[~KT, ~VT]]) ‑> List[Dict[~KT, ~VT]]`
:   

Classes
-------

`DBMigration(config)`
:   

    ### Methods

    `close(self)`
    :

    `connect(self, moduleList: List[str])`
    :

    `dump(self, dataPath: str, transfer: Callable[[List[Dict[~KT, ~VT]]], List[Dict[~KT, ~VT]]] = <function nullTransfer>)`
    :

    `load(self, dataPath: str, transfer: Callable[[List[Dict[~KT, ~VT]]], List[Dict[~KT, ~VT]]] = <function nullTransfer>)`
    :

    `loadData(self, path: str, transfer: Callable[[List[Dict[~KT, ~VT]]], List[Dict[~KT, ~VT]]] = <function nullTransfer>)`
    :