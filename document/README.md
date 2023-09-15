# Xerial Documentation

## Getting Start
- [Tutorial](tutorial/README.md)
- [Data Structure Modification](tutorial/StructureModification.md)
- [One-to-One Relation](OneToOneRelation.md)
- [One-to-Many Relation](OneToManyRelation.md)
- [Many-to-Many Relation](ManyToManyRelation.md)
- [Data dumping and restore with Xerial](DataDump.md)
- [Incremental data backup](IncremetalBackup.md)

## Worth Reading
- [Design and Concept](Concept.md)
- [Special on PostgreSQL](PostgreSQL.md)

## API
- [Xerial API Document](api/xerial/)

## Gaimon

Xerial and [Gaimon MVC Web Application Framework](https://github.com/Piyawanno/Gaimon)
are very tight coupled, since Xerial is designed to be used
in the Gaimon at the first place. Xerial can be used without Gaimon but
Gaimon is strongly depends on Xerial. However, the usage of
Xerial under Gaimon is significantly simplified. Hence, if you
want to use Xerial in the Web Application, we strongly recommend
you to give Gaimon a try.