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
[Structure Modification Procedure](StrucutreModification.md) can be followed.

With this concept, you will always have database structure with your code.

## Always Object/Record as a Whole



## No Join

## Minimal Support of Analytic Feature

## Support for Input Meta Data