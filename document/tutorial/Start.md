# Xerial Tutorial

Example code of this tutorial can be found in example directory.

## Connecting Database

Xerial uses JSON based configuration for connecting database.
For different database vendor, parameter in the JSON configuration is also different. In this tutorial, we use SQLite as database engine due to
the ease of environment setup. JSON configuration for other
database vendors can be found under [database connection configuration]().
Note that in an application we recommend to use [DBSessionPool]()
to make the application independent from database vendor.

To connect to SQLite :

```python
from xerial.SQLiteDBSession import SQLiteDBSession

config = {
	"vendor" : Vendor.SQLITE,
	"database" : "./example.sqlite.bin"
}

session = SQLiteDBSession(config)
session.connect()
```