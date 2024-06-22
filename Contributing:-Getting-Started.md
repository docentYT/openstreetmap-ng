Welcome to the project and thank you for your interest in contributing! This guide will help you get started with the project and provide you with the necessary information to make your first contribution.

## 1. Required Software

OpenStreetMap-NG focuses on simplicity. We use a minimal set of tools to keep the development process straightforward, secure, and easy to understand. The development environment is automatically configured with Nix, and this is the only tool you need to install yourself.

- Nix — [Installation instructions](https://nixos.org/download/)

## 2. Starting the Development Environment

After you have installed Nix, and obtained the project source code, you can enter the development environment by running the following command inside the project directory:

```sh
nix-shell
```

The first time you run `nix-shell`, it will take a little longer than usual. This is because it's downloading and setting up all the necessary packages and tools for the project. But don't worry, future launches will be much faster!

**Important!** Once you are inside the development shell, you can start your preferred code editor **from within it**. This step ensures that your editor will have access to the same Nix environment. Otherwise you will face various file and connection errors.

```sh
# Visual Studio Code:
code .
# PyCharm:
charm .
```

> [!TIP]
> You can automate the `nix-shell` step, by installing an optional [direnv](https://direnv.net) program. We already provide a `.envrc` configuration file that will automatically enter the development shell when you navigate the project directory.

## 3. Starting the Services

During a typical development session, you will most likely need to start the project services, such as the PostgreSQL database. When you are inside the development shell, we provide you with a set of scripts to do just that. The following command will start all necessary services and run the database migrations:

```sh
dev-start
```

Here is a list of running services with short descriptions:

- **postgres**: The primary database service
- **valkey**: An in-memory cache, an open-source fork of redis
- **mailpit**: Local email testing tool, calculates HTML compatibility and spam scores
- **watch-js**: Automatically recompile JavaScript files on change
- **watch-locale**: Automatically recompile translation files on change
- **watch-sass**: Automatically recompile SCSS stylesheet files on change

> [!TIP]
> All custom scripts are defined in the `shell.nix` file. Other useful scripts include `dev-stop` to stop the services, and `dev-clean` to clean services data files.

## 4. Starting the Application

It's time to see OpenStreetMap-NG running!
From your terminal (while still in the development shell), run this simple command to launch the application:

```sh
run  # alias for uvicorn app.main:main --reload
```

You'll know it's working when you see an output in your terminal like:

```log
INFO:     Will watch for changes in these directories: ['/openstreetmap-ng']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [47398] using WatchFiles
INFO:     | 2024-05-18 04:40:09 | root Yarn lock for iD is 054c647
INFO:     | 2024-05-18 04:40:09 | root Yarn lock for @rapideditor/rapid is 2.2.5
INFO:     | 2024-05-18 04:40:09 | root 🐌 Cython modules are not compiled
INFO:     | 2024-05-18 04:40:09 | root 🦺 Running in test environment
...
```

Now head over to your browser and check out your local OpenStreetMap-NG website at <http://127.0.0.1:8000>. Congratulations!

When you're finished exploring, simply press <kbd>CTRL+C</kbd> in your terminal to stop the application.

> [!TIP]
> Something not working? Check out our [troubleshooting](https://github.com/Zaczero/openstreetmap-ng/wiki/Troubleshooting) guide.

## 5. Accessing the Mailbox

We use [Mailpit](https://mailpit.axllent.org) to collect all outgoing mail during development. This makes it easy to view and inspect emails locally. It's ready to use out of the box — no additional configuration required. To open the web interface, simply run the following command in your development shell:

```
open-mailpit
```

There, you will see all collected emails, view HTML compatibility information, check spam scores, and more. This is especially helpful when you're working on new email templates or debugging email-related issues.

## 6. Preloading the Database (Optional)

For some development tasks, you might want to preload the database with some real-world OpenStreetMap data. We make this process easy by providing a script that does everything for you:

```sh
dev-clean  # Clean the database first (recommended)
preload-pipeline
```

The download size is about 6 GB, and the result is cached on your local machine in `data/preload` directory. Subsequent preloads will be able to reuse the cache. The downloader has an auto-updater, which will automatically download newer preload files when available.

The import process takes around 1-2 hours.

> [!IMPORTANT]  
> When preloading the database, it is recommended to have 320 GB of free disk space available.

## 7. Project Structure

It's now a good time to familiarize yourself with the project structure. Here is what you should know:

- **app**: Application code
- **app/alembic**: Database migrations — *we use [alembic](https://alembic.sqlalchemy.org)*
- **app/controllers**: HTTP request handlers
- **app/exceptions**: Exception helpers
- **app/format**: API formatting helpers
- **app/lib**: General-purpose classes and methods
- **app/middleware**: HTTP request middlewares
- **app/models**: Models
- **app/models/db**: Database models
- **app/services**: Database business logic
- **app/static**: Static web assets
- **app/templates**: HTTP response templates
- **app/queries**: Database read-only queries
- **app/validators**: Untrusted user input parsers
- **config**: Configuration files
- **data**: Services data files
- **scripts**: Python scripts (used in `shell.nix`)
- **tests**: Test suite

## Further Reading

The frontend and backend guides have been split into dedicated wiki pages.

- [Contributing: Frontend](https://github.com/Zaczero/openstreetmap-ng/wiki/Contributing:-Frontend)
- Contributing: Backend -- TODO

We also recommend exploring the editor-specific guides:

- [VSCode Recommendations](https://github.com/Zaczero/openstreetmap-ng/wiki/VSCode-Recommendations)