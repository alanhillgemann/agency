# Casting Agency Project

## Table of Contents

* [About](#about)
* [Languages](#languages)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Roles](#roles)
* [Base URL](#base-url)
* [Error handling](#error-handling)
* [Endpoints](#endpoints)
* [Testing](#testing)

## About

This project required me to create an app that allows a production company to manage movies and actors that perform in their movies.

## Languages

* Python

## Dependencies

* PostgreSQL
* Python
* pip

## Installation

```bash
    $ git clone https://github.com/alanhillgemann/agency.git
    $ export DATABASE_URL='postgresql://localhost:5432/agency'
    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ createdb agency
    $ python manage.py db upgrade
    $ flask run
```

## Roles

### casting-assistant

- get:actors
- get:movies
- get:performances

### casting-director

Inherits from casting-assistant, adding:
- post:actors
- patch:actors
- delete:actors
- post:performances
- delete:performances

### executive-producer

Inherits from casting-director, adding:
- post:movies
- patch:movies
- delete:movies

## Base URL

- Local: ```http://localhost:5000/```
- Heroku: ```https://alanhillgemann.herokuapp.com/```

## Error handling

- HTTP Status Codes:
    - 400 - Bad Request
    - 404 - Not Found
    - 422 - Unprocessable Entity
    - 500 - Internal Server Error

- Response Body:
```
    {
        "error": 400,
        "message": "Bad Request"
    }
```

## Endpoints

### GET '/actors'

Returns all actors.
- Request Authorization: ```Bearer token with 'get:actors' permission```
- CURL:
```
    curl http://localhost:5000/actors \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "actors": [
            {
                "age": 57,
                "gender": "male",
                "id": 1,
                "name": "Brad Pitt"
            }
        ]
    }
```

### GET '/actors/:actor_id'

Returns an actor by ID.
- Request Authorization: ```Bearer token with 'get:actors' permission```
- Path Parameters: ```actor_id (int)```
- CURL:
```
    curl http://localhost:5000/actors/1 \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "actor": {
            "age": 57,
            "gender": "male",
            "id": 1,
            "name": "Brad Pitt"
        }
    }
```

### POST '/actors'

Creates an actor.
- Request Authorization: ```Bearer token with 'post:actors' permission```
- Request Parameters:
```
    age (int)
    gender (string)
    name (string)
```
- CURL:
```
    curl http://localhost:5000/actors -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"age": 57, "gender": "male", "name": "Brad Pitt"}'
```
- Response Body:
```
    {
        "actor": {
            "age": 57,
            "gender": "male",
            "id": 1,
            "name": "Brad Pitt"
        }
    }
```

### PATCH '/actors/:actor_id'

Updates an actor by ID.
- Request Authorization: ```Bearer token with 'patch:actors' permission```
- Path Parameters: ```actor_id (int)```
- Request Parameters:
```
    age (int)
    gender (string)
    name (string)
```
- CURL:
```
    curl http://localhost:5000/actors/1 -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"age": 59, "gender": "male", "name": "George Clooney"}'
```
- Response Body:
```
    {
        "actor": {
            "age": 59,
            "gender": "male",
            "id": 1,
            "name": "George Clooney"
        }
    }
```

### DELETE '/actors/:actor_id'

Deletes an actor by ID and associated performances.
- Request Authorization: ```Bearer token with 'delete:actors' permission```
- Path Parameters: ```actor_id (int)```
- CURL:
```
    curl http://localhost:5000/actors/1 -X DELETE \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "deleted": 1
    }
```

### GET '/movies'

Returns all movies.
- Request Authorization: ```Bearer token with 'get:movies' permission```
- CURL:
```
    curl http://localhost:5000/movies \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "movies": [
            {
                "id": 1,
                "release_date": "Fri, 23 Sep 2022 00:00:00 GMT",
                "title": "Bullet Train"
            }
        ]
    }
```

### GET '/movies/:movie_id'

Returns a movie by ID.
- Request Authorization: ```Bearer token with 'get:movies' permission```
- Path Parameters: ```movie_id (int)```
- CURL:
```
    curl http://localhost:5000/movies/1 \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "movie": {
            "id": 1,
            "release_date": "Fri, 23 Sep 2022 00:00:00 GMT",
            "title": "Bullet Train"
        }
    }
```

### POST '/movies'

Creates a movie. Title must be unique. Release date must be in the future.
- Request Authorization: ```Bearer token with 'post:movies' permission```
- Request Parameters:
```
    release_date (datetime)
    title (string)
```
- CURL:
```
    curl http://localhost:5000/movies -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"release_date": "2022-09-23T00:00:00.000Z", "title": "Bullet Train"}'
```
- Response Body:
```
    {
        "movies": [
            {
                "id": 1,
                "release_date": "Fri, 23 Sep 2022 00:00:00 GMT",
                "title": "Bullet Train"
            }
        ]
    }
```

### PATCH '/movies/:movie_id'

Updates a movie by ID. Title must be unique. Release date must be in the future.
- Request Authorization: ```Bearer token with 'patch:movies' permission```
- Path Parameters: ```movie_id (int)```
- Request Parameters:
```
    release_date (datetime)
    title (string)
```
- CURL:
```
    curl http://localhost:5000/movies/1 -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"release_date": "2022-09-30T00:00:00.000Z", "title": "Blonde"}'
```
- Response Body:
```
    {
        "movies": [
            {
                "id": 1,
                "release_date": "Fri, 30 Sep 2022 00:00:00 GMT",
                "title": "Blonde"
            }
        ]
    }
```

### DELETE '/movies/:movie_id'

Deletes a movie by ID and associated performances.
- Request Authorization: ```Bearer token with 'delete:movies' permission```
- Path Parameters: ```movie_id (int)```
- CURL:
```
    curl http://localhost:5000/movies/1 -X DELETE \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "deleted": 1
    }
```

### GET '/performances'

Returns all performances.
- Request Authorization: ```Bearer token with 'get:performances' permission```
- CURL:
```
    curl http://localhost:5000/performances \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "performances": [
            {
                "actor_id": 1,
                "id": 1,
                "movie_id": 1
            }
        ]
    }
```

### POST '/performances/:performance_id'

Creates a performance. Actor ID and Movie ID combination must be unique.
- Request Authorization: ```Bearer token with 'post:performances' permission```
- Request Parameters:
```
    release_date (datetime)
    title (string)
```
- CURL:
```
    curl http://localhost:5000/performances -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"actor_id": 1, "movie_id": 1}'
```
- Response Body:
```
{
    "performance": {
        "actor_id": 1,
        "id": 1,
        "movie_id": 1
    }
}
```

### DELETE '/performances/:performance_id'

Deletes a performance by ID.
- Request Authorization: ```Bearer token with 'delete:performances' permission```
- Path Parameters: ```performance_id (int)```
- CURL:
```
    curl http://localhost:5000/performances/1 -X DELETE \
    -H "Authorization: Bearer $TOKEN"
```
- Response Body:
```
    {
        "deleted": 1
    }
```

## Testing

```bash
    $ python test_app.py
```