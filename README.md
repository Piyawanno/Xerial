# Xerial ORM

A Simple Object Rational Mapping (ORM) library.

## Supported DB
- PostgreSQL
- Oracle
- MariaDB/MySQL
- SQLite
- MS SQL Server

## Installation

With wheel :

```bash
./setup bdist_build
sudo pip3 install dist/xerial-0.9-py3-none-any.whl
```

For development :

```bash
sudo ./setup.py setup
sudo ./setup.py link
```

For production :

```bash
sudo ./setup.py setup
sudo ./setup.py install
```