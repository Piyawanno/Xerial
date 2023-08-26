Module xerial.ExcelWriter
=========================

Classes
-------

`ExcelWriter(modelClass, workbook: xlsxwriter.workbook.Workbook)`
:   

    ### Methods

    `getForeignClause(self, foreignKey: xerial.ForeignKey.ForeignKey) ‑> str`
    :

    `processForeign(self)`
    :

    `writeColumnName(self)`
    :

    `writeForeign(self, foreignKey: xerial.ForeignKey.ForeignKey, cursor)`
    :

    `writeForeignColumnName(self, foreignKey: xerial.ForeignKey.ForeignKey, sheet)`
    :

    `writeForeignSheet(self, cursor, foreignKey: xerial.ForeignKey.ForeignKey, sheet)`
    :

    `writeMain(self, cursor)`
    :

    `writeMainSheet(self, cursor)`
    :

    `writeReference(self)`
    :