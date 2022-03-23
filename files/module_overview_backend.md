# Module overview backend

## app

In app.py is the code for starting our backend.  
If you want to add a route you simply add the route in the section "\# Include all routers".

```python
app.include_router(<new_route>)
```

On startup the application checks if the latest version of the database is used.  
The module has a couple of submodules.

### exceptions

Here are our own exceptions. These are grouped in multiple files according to the subjects that raise them.
In handlers.py you can see what the backend returns when an exception took place. To add a handler of an exception, write it in the `install_handlers` function.

```python
@app.exception_handler(<Exception>)
def <exception>(_request: Request, _exception: <Exception>):
    return JSONResponse(
        status_code=<HTTP status>,
        content={"message": <message>},
    )
```

### logic

These scripts are the gateway between the routers and the database, but they don't add things directly to it. They are grouped by subject.

### routers

Here are all the routers of the API. They only progress the request and send them to their corespondending logic file.  
The submodules of this module have the same names as their URIs.

### schemas

These files contain the input and output models.

### utils

In ```dependencies.py``` are the functions that are used to get models in our database by an ID, to check that someone is authorized, and has the right qualifications for routes and other dependency functions.
Other scripts in this module are things that are needed but don't fit anywhere else.

## database

This module is used for all of our database code.

Our custom code can be found in ```enums.py``` and ```models.py```. The other scripts are for having our database up and running our tests and production.

### enums.py

Here are all our enums, we use these so we don't have any static tables in our database.

### models.py

Here are all the models we need in our database.  
For creating a new model and table in our database, use:

```python
class <NameOfTable>(Base):
    __tablename__ = "<name_of_table>"

    # fields

    # relationships with other models

```

### crud

In these scripts the data in the database is edited. The functions are mostly called from the logic module.
