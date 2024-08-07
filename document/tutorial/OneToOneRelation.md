# One-to-One Relation

Xerial provides features to support relations between tables or Models.
These relations are not coupled with the foreign key of RDBMS but
is an explicit linking between Records. Dropping or changing a parent
record will not have any effect on the child records. With the concept,
the concurrent data handling can be enhanced.

In the term of relation between tables or Models, the One-to-One relation
is the simplest relation. In this case, we have 2 Models. The first Model,
we call it **referee**, which is referenced from the second Model. And we call
the second model **referrer**. The visibility is a key point of this relation,
where the referrer knows the referee but not vise versa. 

In the followed example, the model `Department` is the referee and the
model `Personnel` is the referrer. 

```python
from xerial.DBSessionBase import REGISTER
from xerial.Record import Record
from xerial.IntegerColumn import IntegerColumn
from xerial.StringColumn import StringColumn

@REGISTER
class Department (Record) :
	name = StringColumn(length=128)
	description = StringColumn(length=-1)

@REGISTER
class Personnel (Record) :
	department = IntegerColumn(foreignKey='Department.id')
	firstName = StringColumn(length=128)
	lastName = StringColumn(length=128)
	email = StringColumn(length=64)

session = PostgresDBSession(config).init()
```

Note that, `Personnel` is linked to `Department` with the column
`Personnel.department`. In the database, the column `Personnel.department`
will store the value of `Department.id`. Moreover, the calling of
method `session.checkModelLinking()` with check the correctness of
the linking. If the linked column does not exist, Xerial will print
the warning message to the terminal.

To insert or update data, the referee and the referrer must be independently
ingested :

```python
department = Department()
department.name = 'Production'
department.description = 'This department is responsible to produce the end-product.'

chief = Personnel()
chief.department = department
chief.firstName = 'Garp'
chief.lastName = 'Monkey D.'
chief.email = 'monkey.d.garp@navy.mi.onepiece'

operator = Personnel()
operator.department = department
operator.firstName = 'Koby'
operator.lastName = 'The Hero'
operator.email = 'koby@navy.mi.onepiece'

session.insert(department)
session.insert(chief)
session.insert(operator)

chief.email = 'garp@navy.mi.onepiece'
session.update(chief)
```

Note that the record `chief` and `operator` will be automatically linked
to the record `department`. However, the record `department` must
be firstly inserted before `chief` and `operator`.

By selecting the data, no data will be linked by default. To link
the data with One-to-One relation, the parameter `isRelated` must
be set to `True`. Xerial will be automatically link the data with
optimized query.

Without the linking between models, the data selection can be as
followed implemented:

```python
personnelList = session.select(Personnel, '')
print([i.toDict() for i in personnelList])
```

From the given code, the result will be:

```json
[
	{
		"id": 1,
		"department": 1,
		"firstName": "Garp",
		"lastName": "Monkey D.",
		"email": "monkey.d.garp@navy.mi.onepiece"
	}
]
```

Otherwise, the data between `Personnel` and `Department` can be
linked as followed:

```python
personnelList = session.select(Personnel, '', isRelated=True)
print([i.toDict() for i in personnelList])
```

From the given code, the result will be:

```json
[
	{
		"id": 1,
		"department": {
			"id" : 1,
			"name": "Production",
			"description": "This department is responsible to produce the end-product."
		},
		"firstName": "Garp",
		"lastName": "Monkey D.",
		"email": "monkey.d.garp@navy.mi.onepiece"
	}
]
```

It can be seen that from the relation between `Department` and
`Personnel`, a record of `Department` can be linked to multiple
records of `Personnel`. To be pendant, this is not a strict
One-to-One relation, but can be also used as One-to-Many relation
with one direction visibility. In Xerial, the strict One-to-One
relation is not supported. And for the case of strict One-to-One
relation, we recommend table merge if possible.