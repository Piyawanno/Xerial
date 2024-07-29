# Xerial ORM

A Simple but Powerful Object Rational Mapping (ORM) library.
Xerial is a session-based ORM, which emphasizes the concept
[*Code Centric Data Structure*](document/Concept.md) to support developer
working in team.

For tutorial and documentation see [Document](document/README.md).

For code example see [Example](example).

## Supported DB
- PostgreSQL
- Oracle
- MariaDB/MySQL
- SQLite
- MS SQL Server

## Main Features
- Code Centric Data Structure
- Automatic table creation based on Model Code
- Automatic table structure modification based on Model Code
- Table structure and data rollback
- SQL based query clause
- Relation between models (1-to-1, 1-to-N, N-to-N)
- Metadata for table structure including form input for later use by application development.

## Installation

For production :

```bash
pip3 install xerial-orm
```

For development from source code:

```bash
sudo ./XerialSetup.py setup
sudo ./XerialSetup.py link
```
