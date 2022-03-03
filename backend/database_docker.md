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

The containers can be started using `docker compose up`. You can add the `-d` flag at the end to "detach" the process and let it run in the background, otherwise you'll have to leave your terminal open.

```sh
docker compose up -d
```

### Stopping

```sh
docker compose down
```
