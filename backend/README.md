# Backend

## Setting up a venv

```bash
# Navigate to this directory
cd backend

# Create a virtual environment
python3 -m venv venv

# Make "pip3" and "python3" refer to the custom Python version in your venv
# PyCharm does this automatically, so this is only required if you're using another IDE
source venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Install dev requirements
pip3 install -r requirements-dev.txt
```

Note that, in case your IDE does not do this automatically, you have to run `source venv/bin/activate` every time you want to run the backend, as otherwise your interpreter won't be able to find the packages.

## Creating a .env file

A `.env`-file can be used to store secrets such as database passwords. Further, it allows flexibility among developers by loading a specific configuration from the file instead of hard coding it in.

This directory contains a `.env.example` file which shows the general structure the file should take, with dummy values.

1. Create a new file named `.env` in this directory.
2. Copy the content of the `.env.example` file into it.
3. Edit the environment variables so the values are correct for your local system (e.g. change the password to your database password).

## Keeping requirements up to date

Whenever you'd like to install a new package, make sure to **update the `requirements.txt` or `requirements-dev.txt` files** so that everyone has the same packages installed, and our tests can run easily.

In case your package installs multiple other dependencies, it's not necessary to install those along with it. The main package you installed (along with the correct version) is satisfactory.

## Type annotations

Please **type your code**. Python is not a statically typed language, so IDEs might not be able to provide much useful information. By incorporating type annotations, development becomes a lot easier and faster. Furthermore, this helps avoid unnecessary bugs caused by non-matching types.

```python
def function(first: str, second: int) -> bool:
    pass
```

Link to the documentation for the typing module: https://docs.python.org/3/library/typing.html

## Running the project

To start the API, run the following command in your terminal:

```shell
uvicorn src.app:app --reload
```

The "--reload" argument will enable hot reloading while you're developing, so you don't have to manually restart the process every time.

⚠ ***Note*: the `--reload` argument should *not* be used in production!**

To run the API on a specific IP-address and port, use the `--host` and `--port` arguments:

```shell
uvicorn src.app:app --host 0.0.0.0 --port 80
```