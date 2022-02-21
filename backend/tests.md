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