[![Maintainability](https://api.codeclimate.com/v1/badges/371bc264163d8de4c970/maintainability)](https://codeclimate.com/github/wgarlock/mongo-to-sql/maintainability)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/wgarlock/mongo-to-sql.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/wgarlock/mongo-to-sql/alerts/)
[![codecov](https://codecov.io/gh/wgarlock/mongo-to-sql/branch/main/graph/badge.svg?token=UBMD3BDMFW)](https://codecov.io/gh/wgarlock/mongo-to-sql)
[![Known Vulnerabilities](https://snyk.io/test/github/wgarlock/mongo-to-sql/badge.svg)](https://snyk.io/test/github/wgarlock/mongo-to-sql)
- Introduction

Migrating from MongoDB to Postgresql can be a bit of a nightmare. There are some paid services that can
manage this process for you, but they do much of the schema mapping for you in the end. The goal of this
package is to provide python developers a flexible to tool to migrate there MongoDB database to a SQL database.
This is project currently only supports Postgresql, but the modules could be abstracted and subclassed for Mysql
in the future.

- Use

Prior to running your MongoDB and SQL (Postgresql) database should be running. Your Postgresql database should have no
tables in it.

Excute the conversion

In the mongo_to_sql/process is a simple script to handle the conversion in side of main.py. One should set their
environment variables to execute the conversion. Currently the process is not optimized and does not handle
batch operations. Larger databases could potentially fail. This is a known issue that will be handled in
a new release.

-- Required Environment Varibales

Environment Variables can be placed in .migrate_config if you want to store them outide of your PATH. Below are the
accepted environment variables 

MONGO_HOST=
MONGO_PORT=
MONGO_DBNAME=
MONGO_USER=
MONGO_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DBNAME=
POSTGRES_USER=
POSTGRES_PASSWORD=

- Concepts
Inside of mongo_to_sql/databases/mongo handles the MongoDB abstraction
Inside of mongo_to_sql/databases/postgres handles the Postresql abstraction
Inside of mongo_to_sql/databases/utils are classes that handle column creation
when new tables are being create and value cleaning to make sure the data coming
out of MongoDB can be inserted into the it's respective database table column



