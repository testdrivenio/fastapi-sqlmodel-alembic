# Product API for Tekton

This is REST API
- SQLAlchemy
- SQLModel
- Postgres
- Alembic
- Docker
- Rocketry


## How to setup the project?

You have to have Docker installed in your computer. Then, run the following commands to create the
respective container that includes a fastapi and a postgres container.

```sh
$ docker-compose up -d --build
```

To run the migrations of the database models defined in the project you must the following command
to reflect the changes to the Postgres database
```sh
$ docker-compose exec web alembic revision --autogenerate -m "new migration"
$ docker-compose exec web alembic upgrade head
```

If any wen well you should see the following page after 

```sh
$ curl -d '{"name":"Midnight Fit", "artist":"Mogwai", "year":"2021"}' -H "Content-Type: application/json" -X POST http://localhost:8004/songs
```

## Project

The project has the following structure

```

```

Get all songs: [http://localhost:8004/songs](http://localhost:8004/songs)
