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
    :   Add index to the given column in the existing Model.
        
        Parameters
        ----------
        name: str  name of the column to add index

    `changeLength(self, name: str, length: int)`
    :   Change length of the given StringColumn in the existing Model.
        
        NOTE 1) This method is only allowed for StringColumn.
        
        NOTE 2) For change length of StringColumn from l<256 to l=-1,
        it means that the type of column will be changed.
        Instead of calling changeLength(), changeType will be called. 
        
        Parameters
        ----------
        name: str  name of the column to change type
        length: int new length of the StringColumn to change

    `changeType(self, name: str, column: xerial.Column.Column)`
    :   Change type of the given column in the existing Model.
        
        NOTE 1) Type cannot be arbitrary changed.
        Xerial will check the compatibility between the existing type
        and the given type.
        
        NOTE 2) For change length of StringColumn from l<256 to l=-1,
        it means that the type of column will be changed.
        Instead of calling changeLength(), changeType will be called. 
        
        Parameters
        ----------
        name: str  name of the column to change type
        column: Column attribute of the column to change

    `drop(self, name: str)`
    :   Drop a column from the existing Model.
        
        Parameters
        ----------
        name: str  name of the column to drop

    `dropIndex(self, name: str)`
    :   Drop index from the given column in the existing Model.
        
        Parameters
        ----------
        name: str  name of the column to drop index

    `generateQuery(self) ‑> List[str]`
    :

    `rename(self, oldName: str, newName: str)`
    :   Rename a column in the existing Model.
        
        Parameters
        ----------
        oldName: str  name of the existing column 
        newName: str  desired new name of the existing column