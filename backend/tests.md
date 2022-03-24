# Tests
For tests we use the library [pytest](https://docs.pytest.org/en/7.0.x/) <br>
All tests are written in `tests/test_<module>/test_<file>.py`.


## How to write basic tests
```python
# in src/<module>/<file>.py
def function(x):
    #some code
    return #something

# in tests/test_<module>/test_<file>.py
from src.<file> import *

def test_function(): #important that the tests start with "test_"
    assert function(x) == value
```

## Run the tests
```bash
# Run one file
pytest tests/test_<module>/test_<file>.py

# Run all tests
pytest

# See coverage
coverage run -m pytest
coverage report -m
```

## Requesting fixtures

``fixtures`` are functions that can do or return something before every test. Examples include creating (& tearing down) a database session, etc.

All fixtures in ``tests/conftest.py`` are loaded **automatically** whenever you run `pytest`, so you don't have to import these.

A fixture can be "requested" by adding its name as an argument to your test. For example, to request a `TestClient` you can use the `test_client` fixture:

```python
from starlette.testclient import TestClient

# Request the "test_client" fixture by adding it as a parameter
def test_base_route(test_client: TestClient):
    assert test_client.get("/").status_code == 200
```