# Backend

## Setting up a venv

A `venv` (virtual environment) separates your 

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

## Keeping requirements up to date

Whenever you'd like to install a new package, make sure to **update the `requirements.txt` or `requirements-dev.txt` files** so that everyone has the same packages installed, and our tests can run easily.

In case your package installs multiple other dependencies, it's not necessary to install those along with it. The main package you installed (along with he correct version) is satisfactory.

## Type annotations

Please **type your code**. Python is not a statically typed language, so IDE's might not be able to provide much useful information. By incorporating type annotations, development becomes a lot easier and faster. Furthermore, this helps avoid unnecessary bugs caused by non-matching types.

```python
def function(first: str, second: int) -> bool:
    pass
```

Link to the documentation for the typing module: https://docs.python.org/3/library/typing.html
