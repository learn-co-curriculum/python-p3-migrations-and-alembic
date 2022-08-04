# Migrations and Alembic

## Learning Goals

- Use an external library to simplify tasks from ORM and Advanced ORM.
- Manage database tables and schemas without ever writing SQL through Alembic.
- Use SQLAlchemy to create, read, update and delete records in a SQL database.

***

## Key Vocab

- **Persist**: save a schema in a database.
- **Engine**: a Python object that translates SQL to Python and vice-versa.
- **Session**: a Python object that uses an engine to allow us to
  programmatically interact with a database.
- **Transaction**: a strategy for executing database statements such that
  the group succeeds or fails as a unit.
- **Migration**: the process of moving data from one or more databases to one
  or more target databases.

***

## Introduction

You may have noticed in the curriculum so far that we haven't made many changes
to the database schemas after we started adding data. If you've explored a bit
more on your own, you probably ran into an error telling you that your new
column doesn't exist, or even worse, that an old column cannot be accessed
anymore. This is a familiar problem to most professional programmers, managing
**migrations**.

Alembic is a library for handling schema changes that uses SQLAlchemy to
perform the migrations in a standardized way. Since SQLAlchemy only creates
missing tables when we use the `Base.metadata.create_all()` method, it doesn’t
update the tables to match any changes we made to the columns or keys. Alembic
provides us with classes and methods that will manage schema changes over the
course of development. Because Alembic builds upon the functionality of
SQLAlchemy, it can be used with a wide range of databases and web frameworks.

<details>
  <summary>
    <em>Which class do you need to import to run
        <code>Base.metadata.create_all()</code>?</em>
  </summary>

  <h3><code>declarative_base</code></h3>
  <p><code>declarative_base</code> is imported from the
     <code>sqlalchemy.ext.declarative</code> module.</p>
</details>
<br/>

***

## Creating a Migration Environment

To create a migration environment, create a directory `CH12` and `cd` into
that directory. Next, run `alembic init migrations` command to create a
migration environment in the `migrations/` directory. This process creates our
migration environment as well as an `alembic.ini` file with configuration
options for the environment. If you run `tree` in our directory now, you should
see this structure:

```console
.
├── alembic.ini
└── migrations
    ├── README
    ├── env.py
    ├── script.py.mako
    └── versions
```

The `versions/` directory will hold our migration scripts. `env.py` defines and
instantiates a SQLAlchemy engine, connects to that engine, starts a transaction,
and calls the migration engine. `script.py.mako` is a template that is used when
creating a migration- it defines the basic structure of a migration.

Now that we have created our environment, we need to configure it to work with
our SQLAlchemy app.

***

## Configuring a Migration Environment

`alembic.ini` and `env.py` contain important settings that need to be changed
to work with our database and SQLAlchemy app specifically. `alembic.ini`
contains a `sqlalchemy.url` setting on line 58 that points to the project
database. Since we're starting to make changes to existing databases, we're
going to use a `.db` file instead of working in memory:

```ini
# alembic.ini
sqlalchemy.url = sqlite:///migrations_test.db
```

Next, navigate into `app/db.py` to start designing our database with SQLAlchemy.

```py
# app/db.py

#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///migrations_test.db')

Base = declarative_base()
```

Next, we need to configure `env.py` to point to the metadata attribute of our
new `declarative_base` object. Alembic will use this metadata to compare the
structure of the database schema to the models as they are defined in SQLAlchemy.
First things first, we need to update the path from `app/db.py` so that it is
visible to `env.py`:

```py
# app/db.py

# interact with operating system
import os
# access system parameters
import sys

# add current working directory (cwd) to path
sys.path.append(os.getcwd())
```

Now we can finally update `env.py`:

```py
# migrations/env.py
from app.db import Base
target_metadata = Base.metadata
```

We're all set and ready to make our first migrations. Before we move onto the
next section, run `tree` from the `CH12/` directory and make sure your
directory structure matches the one below:

```console
.
├── alembic.ini
├── app
│   ├── __init__.py
│   └── db.py
└── migrations
    ├── README
    ├── env.py
    ├── script.py.mako
    └── versions
```

***

```py
# python code block
print("statement")
# => statement
```

```js
// javascript code block
console.log("use these for comparisons between languages.")
// => use these for comparisons between languages.
```

```console
echo "bash/zshell statement"
# => bash/zshell statement
```

<details>
  <summary>
    <em>Check for understanding text goes here! <code>Code statements go here.</code></em>
  </summary>

  <h3>Answer.</h3>
  <p>Elaboration on answer.</p>
</details>
<br/>

***

## Instructions

This is a **test-driven lab**. Run `pipenv install` to create your virtual
environment and `pipenv shell` to enter the virtual environment. Then run
`pytest -x` to run your tests. Use these instructions and `pytest`'s error
messages to complete your work in the `lib/` folder.

Instructions begin here:

- Make sure to specify any class, method, variable, module, package names
  that `pytest` will check for.
- Any other instructions go here.

Once all of your tests are passing, commit and push your work using `git` to
submit.

***

## Conclusion

Conclusion summary paragraph. Include common misconceptions and what students
will be able to do moving forward.

***

## Resources

- [Resource 1](https://www.python.org/doc/essays/blurb/)
- [Reused Resource][reused resource]

[reused resource]: https://docs.python.org/3/
