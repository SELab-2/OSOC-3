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

These scripts are the gateway between the API and the database but they don't add things directly to it. They are grouped by the subject of each in the database.

### routers

### schemas

### utils

## database

### crud

## tests