# Structure Modification

In the development process, the data structure can be changed
in each iteration. Data structure modification is an inconvenient
task, since the developer and/or the database administrator
must know, in which table and how data structure will be changed.
The modification must also consider about the data integrity and
the backup plan. In some case, data structure modification can crash
the entire system in the deployed environment. In the worst case,
data lost can be experienced.

To solve this problem, Xerial provides automatic data structure modification integrated with the code. As an example a simple Model of a Book will created with the followed code :

```python

from xerial.Record import Record
from xerial.StringColumn import StringColumn

class Book (Record) :
	name = StringColumn(length=64)
	author = StringColumn(length=-1)
```

This code snippet is defined as the `version 1.0` of the Book Model.
Afterwards, the developer finds out that Book should have the name
of the publisher. Publisher column can be directly added to the model.
Moreover, the method `modify()` must be implemented in the Model
to get the automatic structure modification. In this method, the version
if the new structure must be defined and with the structure modification.

```python

from xerial.Record import Record
from xerial.StringColumn import StringColumn

class Book (Record) :
	name = StringColumn(length=64)
	author = StringColumn(length=-1)
	publisher = StringColumn(length=64)

	def modify(self) :
		modification = self.createModification('1.1')
		modification.add('publisher', StringColumn(length=64))

```

In the first step, the `modification` object must be created
by given the version number. Note that the version number is
based on the version system provided from the module
[packaging.version](https://pypi.org/project/packaging/).
The first modification must have the version `> 1.0`.
The modification will be used to modify the structure of Model
from the latest version to the current version.
For detail, please, see [Modification API](api/xerial/Modification.md).

To execute the modification, the method
[DBSessionBase.checkModification()](api/xerial/DBSessionBase.md) or
[AsyncDBSessionBase.checkModification()](api/xerial/AsyncDBSessionDBSessionBase.md) or
must be called, whereas all modifications of registered Model will
be automatically executed. Followed is the example :

```python

from xerial.Record import Record
from xerial.StringColumn import StringColumn

class Book (Record) :
	name = StringColumn(length=64)
	author = StringColumn(length=-1)
	publisher = StringColumn(length=64)

	def modify(self) :
		modification = self.createModification('1.1')
		modification.add('publisher', StringColumn(length=64))

config = {
	"vendor" : Vendor.SQLITE,
	"database" : "./example.sqlite.bin"
}

session = SQLiteDBSession(config)
session.connect()
session.appendModel(Book)
session.createTable()
session.checkModification('/var/xerial/ModelVersion.json')
```

Model can be multiple time modified. But the version of each
modification must be increased. We also recommend that the modification
code should not be changed. Otherwise, the correctness of
structure modification cannot be guaranteed. The followed is example
code for multiple modification.

```python

from xerial.Record import Record
from xerial.StringColumn import StringColumn
from xerial.IntegerColumn import IntegerColumn

class Book (Record) :
	name = StringColumn(length=128)
	author = StringColumn(length=-1)
	publisher = StringColumn(length=64)
	edition = IntegerColumn(length=64)

	def modify(self) :
		modification = self.createModification('1.1')
		modification.add('publisher', StringColumn(length=64))
		modification = self.createModification('2.0')
		modification.changeLength('name', 128)
		modification.add('edition', IntegerColumn())

```
