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
# search file for target_metadata (line 21)
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

## Generating our First Migration

Let's start off with creating a base, empty migration. Make sure you are in
the `CH12/` directory and run the following command:

```console
% alembic revision -m "Empty Init"
  Generating .../python-p3-migrations-and-alembic/CH12/migrations/versions/6b9cb35ba46e_empty_init.py ...  done
```

You should notice that a new file has popped up in the `migrations/versions/`
directory. Here's what you should see inside:

```py
"""Empty Init

Revision ID: 6b9cb35ba46e
Revises: 
Create Date: 2022-08-04 13:21:26.936909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b9cb35ba46e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
```

This file starts off with the message that we included with our `alembic`
command. It is important to treat these messages as you would commit messages
in Git so that other developers know when certain tables, columns, keys, and
so on were added to the database.

The `upgrade()` method includes the code that would be needed to perform
changes to the database based on this migration. Similarly, the `downgrade()`
method includes any code that would be needed to undo this migration and return
to the previous state.

Were there to be any changes in our migration, we would run the following
command:

```py
% alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 6b9cb35ba46e, Empty Init
***
```

This upgrades the database to the `head`, or newest revision.

Now that we've laid down a base for our migrations, we can begin adding data
to our SQLAlchemy app. When we make changes to data models, we can use Alembic
to automatically generate migrations for us and upgrade the database
accordingly.

## Autogenerating a Migration

Now let's add our data model to `app/db.py`. We'll keep working with the
`Student` model from previous lessons.

```py
# app/db.py
import os
import sys

sys.path.append(os.getcwd())


from datetime import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy import (CheckConstraint, UniqueConstraint,
    Column, DateTime, Integer, String)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///migrations_test.db')

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        UniqueConstraint('student_email',
            name='unique_email'),
        CheckConstraint('student_grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'))

    student_id = Column(Integer(), primary_key=True)
    student_name = Column(String(), index=True)
    student_email = Column(String(55))
    student_grade = Column(Integer())
    student_birthday = Column(DateTime())
    student_enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.student_id}: " \
            + f"{self.student_name}, " \
            + f"Grade {self.student_grade}"
```

<details>
  <summary>
    <em>Note that we are no longer including the shebang. Why is that?</em>
  </summary>

  <h3>This file will not be executed as a script.</h3>
  <p>The shebang tells the command line where to find the interpreter for the
     code in a file. It is only necessary for code that you want to execute
     from the command line without the <code>python</code> keyword.</p>
</details>
<br/>

With our `Student` model added in, we can now create a migration to add the
`students` table to our database. This is a simple migration, so we can take
advantage of Alembic's ability to generate the code for us automatically:

```console
% alembic revision --autogenerate -m "Added Student model"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'students'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_students_student_name' on '['student_name']'
  Generating /Users/benbotsford/Documents/new-curriculum/intro-to-sqlalchemy/python-p3-migrations-and-alembic/CH12/migrations/versions/361dae855898_added_student_model.py ...  done
```

During autogeneration, Alembic inspects the metadata of `Base` in `db.py`,
comparing it to the current state of the database. In the command above,
Alembic detected that we added a model for a `students` table. It also detected
that we added an index on `student_name` to speed up searches by name.

Let's take a look at the new migration file:

```py
"""Added Student model

Revision ID: 361dae855898
Revises: 6b9cb35ba46e
Create Date: 2022-08-04 14:21:32.441071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '361dae855898'
down_revision = '6b9cb35ba46e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('student_name', sa.String(), nullable=True),
    sa.Column('student_email', sa.String(length=55), nullable=True),
    sa.Column('student_grade', sa.Integer(), nullable=True),
    sa.Column('student_birthday', sa.DateTime(), nullable=True),
    sa.Column('student_enrolled_date', sa.DateTime(), nullable=True),
    sa.CheckConstraint('student_grade BETWEEN 1 AND 12', name='grade_between_1_and_12'),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('student_email', name='unique_email')
    )
    op.create_index(op.f('ix_students_student_name'), 'students', ['student_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_students_student_name'), table_name='students')
    op.drop_table('students')
    # ### end Alembic commands ###
```

There are a few important things to note here. First, a `down_revision` has been
added. This points to the ID for the previous migration file. We can also see
that the `upgrade()` and `downgrade()` methods have been filled out. The syntax
is very similar to that of a SQLAlchemy ORM model- columns, data types,
constraints and so on are defined by classes imported via the `sqlalchemy`
module. Alembic then executes these instructions using its own `op` class.

Now we can run the autogenerated migration and create the `students` table:

```console
% alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 6b9cb35ba46e -> 361dae855898, Added Student model
```

Open up `migrations_test.db` and you should see two tables: `alembic_version`,
which stored the migration ID for the current state of the database, and
`students`, which contains all of the columns, keys, and constraints that we
included in our model!

![Table `students` with columns: `student_id`, `student_name`, `student_email`,
`student_grade`, `student_birthday`, and `student_enrolled_date`.](https://curriculum-content.s3.amazonaws.com/python/studentsdb.png
"students table")

***

## Instructions

If you have not already, run `pipenv install` to create your virtual
environment and `pipenv shell` to enter the virtual environment.

- Add a column to the `Student` model.
- Autogenerate a migration using Alembic.
- Upgrade your database schema with `alembic upgrade head`.

Once your database schema has been upgraded, commit and push your work using
`git` to submit.

***

## Conclusion

Managing migrations is an important skill for a full-stack developer to keep
in their toolbox. Alembic is a powerful tool for carrying out migrations and
can handle most tasks automatically. That being said, Alembic can't do
_everything_ on its own. In the next lesson, we will explore how to manually
configure migrations and downgrade to revert to an earlier state.

***

## Resources

- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/14/orm/)
- [SQLAlchemy ORM Column Elements and Expressions](https://docs.sqlalchemy.org/en/14/core/sqlelement.html)
- [Tutorial - Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
