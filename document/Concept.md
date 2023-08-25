# Xerial Design anc Concept

## Code Centric Data Structure

One of major problems, which developers regularly face, is the definition
of database structure used in the project. Without additional tools or libraries,
the responsible mostly directly creates tables into database. In the lucky
case, other developers in the team can eventually find document in form of SQL file
or ER-diagram somewhere else. Otherwise, they have to logged into database
type some command to get database structure. This problem can escalate,
by modification of database structure, which can be a daily task of someone
in the team. Hence, a proper procedure must be created to keep database structure
of everyone in the team updated. To solve this problem, some team decides to
use centralized database and each team member have to connect to this database
for software development. This solution, however, causes other problems e.g.
someone accidentally modifies data or structure and has a affect on code of
the other. Moreover, many pieces of code can be affected by the structure
modification.

Object Relation Mapping (ORM) but not all ORM can solve this problem. Some ORM,
especially with Active Record pattern, orients on data-structure in the
database. It means that, database table must be firstly created and
ORM will automatically find out, how tables are defined. For this kind
of ORM, the described problem cannot be solved. Other ORM defines
database structure in an external source i.e. in XML file or JSON file.
This concept can solve the described problem but still can cause a side effect
namely the single source of truth, where the external structure definition
does not match to the class/object attributes.

Hence, by design, database or table structure will be defined directly
in the code so that each class, which inherits from **Record** class,
corresponds a table in the database.
**Some** of class attributes will be used as a column of the table.
To define, which class attribute is a column of table, the attribute
must be instance of **Column** inherited class. Name of class attribute
will become name of the column. The attribute itself can have meta data
for database configuration or for other purposes. After mapping class
to **DBSession**, the class attribute will be stored in **meta**.
And object created from these classed will have a regular attributes
not the meta attribute defined in the class. See [Tutorial](tutorial/Start.md)
for more detail. By modification of database structure,
[Structure Modification Procedure](StructureModification.md) can be followed.

With this concept, you will always have database structure with your code.

## Always Object/Record as a Whole

In the regular SQL, developer can select specific columns from the table.
Not entire columns must be selected at once. The advantage of this method
is that the data transfer over network can be spared and eventually
the performance can be improved in comparison to
`SELECT * FROM MyTABLE`. The problem using this feature is
the discrepancies of the source code and the consumption of the data.
For each case of usage, the data structure of output must be carefully defined.
The change of the data structure can lead to errors and can be very
difficult to debug. To avoid the problem, Xerial is designed to be unified
for the entire code base. The structure of the data is defined by **Model**
only there and no where else. Hence, the output always has the complete
Object/Record. Or in other words, all columns of a table will be selected
as a whole. No matter, what kind of data consumption, there are only 2 types
of data structure from Xerial :

1. Object or Record defined be Model
2. List of Object or Record : It must be list and not set or dict because
the sequence of the selected data must be kept e.g. `ORDER BY` statement.

For the further structure can be lately processed :

```python
recordMap = {i.id:i for i in recordList}
```

## No Join

`JOIN` is an essential feature of SQL to retrieve data across tables.
In most project with SQL, `JOIN` is intensively used. Beside the mentioned problem with the data structure, `JOIN` can cause other problem
in the software development. The SQL code with `JOIN` can be very complex
and hard to understand and hence hard to debug. By structure modification,
the related source code with `JOIN` must be accordingly modified and tested.
Moreover, `JOIN` on huge amount of data or across many tables can consume
the whole resource of database and significantly slow down the whole system.
In other words, `JOIN` can potentially cause performance problem.

Hence, Xerial is designed to use **Explicit Aggregation** instead of `JOIN`.
For the **Explicit Aggregation**, the relation between table can be created
: **1:1, 1:N, N:N** using parameter `foreignKey='OtherTable.id'` in
each attribute of Model or the attribute with the type
`Children('ChildTable.id')` of the Model. By selecting data,
Xerial will select data from each table separately with optimized SQL query
command and aggregate/fuse data from each table according to data structure 
defined in Model. For each related Record, the whole Record will be fetched
from the database.

With **Explicit Aggregation**, Xerial trades of the increasing number
of query and database connection with the unified data structure.
However, from many test, benchmark and use case, we find out that
**Explicit Aggregation** generally provide a significant better performance
in comparison to `JOIN`.

## Minimal Support of Analytic Feature

SQL can be used as a data analytic tool using provided analytic statement
e.g. MAX, MIN, SUM, COUNT, etc.. The advantage of this approach is
minimizing data transfer because data can be directly analyzed where they
are stored. SQL is, however, a stateless query language, where data
disappear at the end of the statement. Combined statement or store procedure
or procedure extension e.g. PL/SQL can be used. Nevertheless, SQL
is not a dedicated programming language. Data analytic with SQL
can be very complex, difficult to used and difficult to debug.

Hence, Xerial supports and will support only minimum analytic features.
In our opinion, database should be preferably used for data storage
and data query. Data analytic should be properly done with dedicated
programming language like Python.

## Support for Input Meta Data

In general, the data structure in database and the user input
are strongly coupled. From many years of our experience, we find out that

1. Developer spends a lot of time to develop user input according
to data structure. This is a kind of grind work.
2. The small discrepancy between user input and data structure can
easily cause a difficult to find bug for example the name of input
and attribute of data.
3. Modification of data structure means modification of user input.

In the team with the work separation based on capability of developers
e.g. front-end, back-end, database management, the integration of work
can be very complicated, since the coupled works are developed separately.
In some case, the integration becomes never ending process and takes
longer than the development of each part.

By design, Xerial couple the data structure with the user input by
giving the meta data of the input into the attribute of the Model
with parameter `input=Input()`. To extract the input meta data,
the static method `Model.extractInput()` can be called, which
provide meta data of user input according to data structure.
The input meta data will not directly generate the user input form
but can be used by other library or framework e.g. Gaimon MVC Web Framework,
which not only generate the user input form but also map the data
from user input to the Record for the further process like inserting
or updating data. As a result, by modification of data structure,
the other parts of the software will be automatically changed accordingly
and errors can be minimized.

## Soft Foreign Key

Foreign Key in the relational database with ACID compliance is an essential
feature but can be burden at the same time. The database with foreign keys
in the high concurrency environment can experience a database lock, where
the whole operation cannot be executed until the database is restarted.

To avoid database lock problem, Xerial does not use the foreign key feature
of the database instead it links data between table with **Explicit Aggregation**
concept. Moreover, we recommend not to delete the actual data especially
the data with the relation to other table. (Which one does not have?)
In stead of data deletion, we recommend to use `isDrop` flag as an attribute
of the Model. With the concept, it cannot cover the whole desire behavior of
foreign key, however, it can give the developer to safely link between
table and completely avoid the database lock caused by foreign key usage.
