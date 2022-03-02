# Setting up and running a local database instance

This document explains how to start a local MariaDB database for development using Docker.

## Installing Docker

Install instructions for:

- [Linux (per distribution)](https://docs.docker.com/engine/install/#server)
- [Mac](https://docs.docker.com/desktop/mac/install/)
- [Windows (using WSL)](https://docs.docker.com/desktop/windows/install/)

## Installing Docker-Compose (Linux)

This step is only required on Linux, **not on Mac or Windows**.

Follow the instructions in [Docker's README](https://github.com/docker/compose#linux).

## Starting and stopping the database

### Starting

The containers can be started using `docker compose up`. We have, however, created configuration files for both development and production, so you have to pass in the path to those files to override the default configurations.

```sh
# Development environment
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production environment
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Stopping

```sh
docker compose down
```
