# High level documentation of the architecture and design

This files gives a short description of the used architecture and the design of the project.

## Architecture
A visual representation of our architecture is described in the **deployment diagram**.

### Presentation Layer

To make the pages that the end users will see, we use TypeScript with the React framework. This calls the domain layer.

### Domain Layer

To provide the data to the presentation layer in a structured way via an API, we use Python 3.10.2 with the FastAPI framework.

### Persistence Layer

To call the database, and to be able to use the data easily in the domain layer, we use an ORM called SQLAlchemy.

### Database Layer

The underlying database technology we use to finally store the data is MariaDB.

## Design
The sequence diagrams of our application can be found [here](https://github.com/SELab-2/OSOC-3/tree/develop/files).
In those diagrams, the most important interactions between objects are shown.
