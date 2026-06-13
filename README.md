# YouRL

[![Tests](https://github.com/dxxdpool/YouRL/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/dxxdpool/YouRL/actions/workflows/tests.yml)

A URL shortener built with **FastAPI**, **PostgreSQL**, and **Redis**.

## Features
- JWT authentication
- URL shortening
- URL expiration support
- Click analytics
- Redis-backed rate limiting
- Integration tests with pytest

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Alembic
- Docker & Docker Compose
- Pytest

## Running the Project
### Prerequisites
 - Docker Desktop
 - Python 3.11+
 - uv

a. Start the services:
```bash
docker compose up -d --build
```

b. Apply database migrations:
```bash
docker compose exec backend uv run alembic upgrade head
```

c. Access the API:
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running Tests

```bash
uv run pytest
```