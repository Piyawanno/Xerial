# One-to-Many Relation

One-to-Many is very similar to [One-to-One Relation](OneToOneRelation.md).
The only difference from Ont-to-One is that in the One-to-Many,
the **referee** and the **referrer** knows each other.

```python

from xerial.DBSessionBase import REGISTER
from xerial.Record import Record
from xerial.IntegerColumn import IntegerColumn
from xerial.StringColumn import StringColumn
from xerial.Children import Children

@REGISTER
class Department (Record) :
	name = StringColumn(length=128)
	description = StringColumn(length=-1)
	personnel = Children('Personnel.id')

@@REGISTER
class Personnel (Record) :
	department = IntegerColumn(foreignKey='Department.id')
	firstName = StringColumn(length=128)
	lastName = StringColumn(length=128)
	email = StringColumn(length=64)

session = PostgresDBSession(config).init()
```

Note that the only difference of the code is `personnel = Children('Personnel.id')`,
which has no effect on data structure in the database. In this column,
the code designates that `Department` as referee will link to `Personnel`
as the referrer with the column `id` of `Personnel` and from
`department = IntegerColumn(foreignKey='Department.id')`, `Personnel` will
link back to `Department.id`.

By ingesting data, unlike One-to-One relation, data between referee and referrer
will be automatically linked.

```python

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

department = Department()
department.name = 'Production'
department.description = 'This department is responsible to produce the end-product.'
department.personnel = [chief, operator]

session.insert(department)

department.name = 'Production Department'
session.update(chief)
```

To select the referrer, there is no difference between Ont-to-One and
One-to-Many. However, if the referee is selected and the parameter `hasChildren`
is set to `True`, the related records of referrer will be also selected
and data are automatically linked.

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

```python
departmentList = session.select(Department, '', hasChildren=True)
print([i.toDict() for i in departmentList])
```

From the given code, the result will be:

```json
[
	"department": {
		"id" : 1,
		"name": "Production",
		"description": "This department is responsible to produce the end-product.",
		"personnel": [
			{
				"id": 1,
				"firstName": "Garp",
				"lastName": "Monkey D.",
				"email": "monkey.d.garp@navy.mi.onepiece"
			}, {
				"id": 1,
				"firstName": "Koby",
				"lastName": "The Hero",
				"email": "koby@navy.mi.onepiece"
			},
		]
	},
]
```

Like the other part of Xerial, the query for selecting data with the
link between the referee and the referrer is optimized. In the given
example 2 queries will be executed to retrieve the result. Note that
in normal case, Xerial will link Models in maximum 2 vertical layers and no more
to prevent the circular linkage. From the best practice, the relation
over 2 layers can complicate the data management and should be avoided.
If it is necessary, we recommend manually lik between Models in different layers.
Many-to-Many is the exception to this rule.