# FastAPI + SQLModel + Alembic

Sample FastAPI project that uses async SQLAlchemy, SQLModel, Postgres, Alembic, and Docker.

## Getting Started

```sh
$ docker-compose up -d --build
$ docker-compose exec web alembic upgrade head
```

Sanity check: [http://localhost:8004/ping](http://localhost:8004/ping)

Add a song:

```sh
$ curl -d '{"name":"Midnight Fit", "artist":"Mogwai", "year":"2021"}' -H "Content-Type: application/json" -X POST http://localhost:8004/songs
```

Get all songs: [http://localhost:8004/songs](http://localhost:8004/songs)
