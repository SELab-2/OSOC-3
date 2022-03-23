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

Here are our own exceptions we raise. Each exception are grouped in the scripts according to the subject when they are raised  
In handlers.py you find what the backend return when a exception took place. To add a handler of an exception you write in the install_handlers function

```python
@app.exception_handler(<Exception>)
def <exception>(_request: Request, _exception: <Exception>):
    return JSONResponse(
        status_code=<HTTP status>,
        content={"message": <message>},
    )
```

### logic

These scripts are the gateway between the routers and the database, but they don't add things directly to it. They are grouped by the subject of each in the database.

### routers

Here are all the routers of the API. They only progress the request and send them to their corespondending logic file.  
The sub modules of this module are the same of the URI.

### schemas

These files contains the input and output models.

### utils

In ```dependencies.py``` are the functions that are used to get models in our database by and ID, is authorized, and has the right qualifications for routes.  
Other scripts in this module are things that are needed but don't fit anywhere else

## database

This module is used for all our database code

our costum code is find in ```enums.py``` and ```models.py```. The other scripts are for having our database up and running in our tests and production.

### enums.py

Here are all our enums, it's used to not have a static table in our database.

### models.py

Here are all the models we need have in our database.  
For creating a new model and table in our database u use:

```python
class <NameOfTable>(Base):
    __tablename__ = "<name_of_table>"

    # fields

    # relationships with other models

```

### crud

In these scripts the data in the database is edited. The functions are mostly called from the logic module.
