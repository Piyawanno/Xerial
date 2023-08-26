Module xerial.Modification
==========================

Functions
---------

    
`generateColumn(column, hasDefault=True)`
:   

Classes
-------

`Modification(version: str, table: str, meta: list, vendor: xerial.Vendor.Vendor)`
:   

    ### Methods

    `add(self, name: str, column: xerial.Column.Column)`
    :   Add a column into the existing Model.
        
        Parameters
        ----------
        name: str  name of the added column
        column: Column attribute of the added column

    `addIndex(self, name: str)`
    :

    `changeLength(self, name: str, length: int)`
    :

    `changeType(self, name: str, column: xerial.Column.Column)`
    :

    `drop(self, name: str)`
    :

    `dropIndex(self, name: str)`
    :

    `generateQuery(self) ‑> List[str]`
    :

    `rename(self, oldName: str, newName: str)`
    :