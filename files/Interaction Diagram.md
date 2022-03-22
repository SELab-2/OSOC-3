# Interaction Diagram

## Main application

The main application contains the FastApi routers. It loads and adds the various routers.

## Routers

Each router processes the path and query parameters and the body of a request. These are passed to the logic layer.

## Wrapping

To return the database objects to the API, we first wrap them into API-friendly objects (Pydantic). This also ensures that when something goes wrong, there is a clear error. The wrapping is also done in the other direction: the body of a request is first wrapped in a Pydantic model. This allows us to perform validation of fields, and also makes the body easier to work with. The arguments are extracted in the logic layer and passed to the Crud layer.

## Logic

The logic layer is the link between the database and routers. This layer provides a strict split between to API and database logic. The logic layer will be called by a router and then call the appropriate functions from the crud layer.

## Crud

The crud layer connects to the database via a Session. This layer will modify or query the database via our ORM. Any retrieved data goes back through the logic layer to the router.

## Database

The crud layer will use an ORM session to create, read, update or delete data in the database.



![interaction diagram](.\interaction_diagram.png)