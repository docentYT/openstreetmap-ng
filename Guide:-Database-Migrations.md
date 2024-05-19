We use [alembic](https://alembic.sqlalchemy.org) to automate changes to our database structure.

## Creating a Migration

When you make changes to the code that affect the database (like adding or modifying tables), you'll need to create a migration file.
First, run the following command:

```sh
alembic-migration
```

You'll be asked to provide a descriptive name for the migration (e.g., "Add users table"). Alembic will then generate an automatic migration file in the **app/alembic/versions** directory. This file **will require** your attention and fixes.

> [!TIP]
> You can skip the naming prompt by providing the name directly in the command: `alembic-migration "<name>"`

## Applying Migrations

Migrations are applied automatically when you start the database as part of the `dev-start` command.
If you've made changes and need to update the database, simply restart the helper services using the `dev-restart` command.