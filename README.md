# OSOC-3

## Table of Contents

[User manual](#user-manual)

[High level documentation of the architecture and design](#high-level-documentation-of-the-architecture-and-design)

[Local Setup Instructions](#local-setup-instructions)

- [TLDR](#tldr)
- [Frontend](#frontend)
  - [Installing Node.js and dependencies](#installing-nodejs-and-dependencies)
  - [Starting Frontend](#starting-frontend)
  - [Frontend Tests](#frontend-tests)
  - [Building Frontend](#building-frontend)
- [Backend](#backend)
  - [Installing Docker and MariaDB](#installing-docker-and-mariadb)
  - [Installing Python and dependencies](#installing-python-and-dependencies)
  - [Starting the database](#starting-the-database)
  - [Starting Backend](#starting-backend)
  - [Running Tests](#running-tests)
  - [Database Migrations](#database-migrations)
  - [Adding the initial admin](#adding-the-initial-admin)

## User manual

The user manual can be found [here](files/user_manual.pdf).

## High level documentation of the architecture and design

Documentation about the architecture and design can be found [here](files/documentation_architecture_and_design.pdf).

## Local Setup Instructions

Below are the instructions on how to set up the frontend and backend. Instructions for backend should be executed in the `/backend` directory, and instructions for frontend should be executed in the `/frontend` directory.

### TLDR

#### Frontend

- Install `Node v16.14`

- Install Yarn (`npm install --global yarn`)

- Install the dependencies (`yarn install`)

- Available scripts:

  ```shell
  # Running
  yarn start
  
  # Testing
  yarn test
  
  # Linting
  yarn lint
  
  # Building (for production)
  yarn build
  ```

#### Backend

- Install `Python 3.10.2`

- Install `Docker Engine` (through `Docker Desktop` if not on Linux)

- Install `MariaDB` drivers & connectors

- Create a `Virtual Environment` (`python3 -m venv venv`)

- Install the dependencies (`pip3 install -r requirements.txt -r requirements-dev.txt`)

- Required scripts:

  ```shell
  # Activate your Virtual Environment
  source venv/bin/activate

  # Start the Docker container to run the database
  docker compose up -d

  # Stop the Docker container
  docker compose down
  ```

- Available scripts:

  ```shell
  # Running
  uvicorn src.app:app
  
  # Running with hot reloading
  uvicorn src.app:app --reload
  
  # Database migrations: updating to most recent version
  alembic upgrade head
  
  # Database migrations: generating a new revision
  alembic revision --auto-generate -m "Your message here"
  
  # Testing
  pytest .
  
  # Testing + coverage report
  pytest --cov=src .
  
  # Linting
  pylint src
  
  # Static type checking
  mypy src
  ```

### Frontend

#### Installing Node.js and dependencies

1. Install `Node.js v16.14` if you don't have it already (check using `node --version`)

   - Windows: https://nodejs.org/en/download/

   - Linux, MacOS, and WSL 2: use [`nvm (recommended)`](https://github.com/nvm-sh/nvm#install--update-script) or install [manually](https://nodejs.org/en/download/)

     After installing `nvm` (and adding it to your `$PATH` or `.bashrc/.zshrc` file), you can install the required version using the command below:

     ```shell
     # Install the required Node version
     nvm install 16.14.1
  
     # Make your shell use the newly-installed version
     nvm use 16
     ```

2. Install the Yarn package manager

   ```shell
   npm install --global yarn
   ```

3. Install the dependencies

   ```shell
   yarn install
   ```

#### Running Frontend

Starting the frontend is very simple. All you have to do is run the command below:

```shell
yarn start
```

and the website should open automatically in your browser. In case it doesn't, navigate to `http://localhost:3000/`.

#### Frontend Tests

```shell
# Tests
yarn test

# Linting
yarn lint
```

#### Building Frontend

The build files will be written to `/build`.

```shell
yarn build
```

### Backend

#### Installing Docker and MariaDB

1. Install Docker Engine and Docker Compose by following the official installation instructions

    Note: Docker Desktop installs both Engine and Compose. However, this is only available on MacOS & WSL2. Linux users will have to manually install both of these tools.

   - Linux (choose your distribution):
      - Docker Engine: https://docs.docker.com/engine/install/#server)
      - Docker Compose: https://docs.docker.com/compose/install/
   - MacOS: https://docs.docker.com/desktop/mac/install/
   - Windows (**needs WSL 2**): https://docs.docker.com/desktop/windows/install/#wsl-2-backend

2. Install the MariaDB drivers & connectors
   - Linux and WSL 2: `sudo apt install libmariadb3 libmariadb-dev`
   - MacOS: `brew install mariadb`

#### Installing Python and dependencies

1. Install Python 3.10.2 if you don't have it already (check using `python3 --version`)

- Windows: https://www.python.org/downloads/release/python-3102/

- Linux, MacOS and WSL 2: use [`pyenv (recommended)`](https://github.com/pyenv/pyenv#installation) or install [manually](https://www.python.org/downloads/release/python-3102/)

  After installing `pyenv` (and adding it to your `$PATH` or `.bashrc/.zshrc` file), you can install the required version using the command below:

  ```shell
  pyenv install 3.10.2
  ```

  You don't have to manually change your Python version afterwards. `Pyenv` should pick it up automatically thanks to the [`.python-version`](backend/.python-version) file in the `/backend` directory.

2. Create a [`Virtual Environment`](https://docs.python.org/3/tutorial/venv.html) to install your packages in

   ```shell
   # Create a new Virtual Environment
   python3 -m venv venv

   # Activate it
   source venv/bin/activate
   ```

3. Install the regular dependencies and development dependencies

   ```
   pip3 install -r requirements.txt -r requirements-dev.txt
   ```

For all commands below, make sure your `Virtual Environment` is activated at all times. Otherwise, your Python interpreter won't be able to find the correct package.

#### Starting The Database

We use `Docker` containers to run the database server for local development. The credentials used for this container are not secure, but this doesn't matter as they are only used for local development. The container can be started using the following command:

```shell
docker compose up -d
```

and stopped using:

```shell
docker compose down
```

#### Starting Backend

First, make sure your `Docker` container is running so that the app can connect to the database. See [Starting The Database](#starting-the-database) for more info.

```shell
uvicorn src.app:app
```

For local development, you can enable `hot reloading` by passing the `--reload` option:

```shell
uvicorn src.app:app --reload
```

**Note**: `--reload` should only be used in development, and _**not**_ when hosting the application on a server!

#### Running Tests

```shell
# Tests
pytest .

# Tests + coverage report
pytest --cov=src .

# Linting
pylint src

# Type checking
mypy src
```

#### Database Migrations

```shell
# Updating the current state of the database to the latest version
alembic upgrade head

# Generating a new revision
alembic revision --autogenerate -m "Your message here"
```

Keep in mind that auto-generated migrations may need manual editing in some edge cases. Always check if you can still upgrade to head, and if the tests still run ([Running Tests](#running-tests)). One of our tests tries to go through every migration in history to the most recent one and back down, in order to verify that all migrations work in the testing environment as well.

More info on upgrading and downgrading (such as relative upgrades) can be found in [`Alembic's documentation`](https://alembic.sqlalchemy.org/en/latest/tutorial.html#relative-migration-identifiers)

#### Adding the initial admin

When starting from an empty database, there are no admins yet to create (or accept) pending requests. You can add an admin manually using the [`create_admin.py`](/backend/create_admin.py) script.

```sh
python3 create_admin.py --name name_here --email email@address.here
```

The script will then show a prompt asking for the admin's password, and another one asking for confirmation. The keys you press are hidden, so the password is not visible in your terminal.
