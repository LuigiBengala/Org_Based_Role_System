# Organization Based Role Access System

A FastAPI service for managing organization-scoped users, studies, and sessions with role-based access control. The API's interactive documentation is available at `/docs` when the service is running.

## Requirements

- Python 3.13
- PostgreSQL
- Docker (for the container workflow)

## Run locally (without Docker)

Start PostgreSQL and create the application database:

```bash
createdb -h localhost -p 5432 -U postgres occam
```

Create and activate a Python 3.13 virtual environment, then install the dependencies:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create `.env` in the repository root with your local PostgreSQL credentials and a development-only signing key:

```dotenv
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your-local-database-password
DATABASE_NAME=occam
DATABASE_USERNAME=postgres
SECRET_KEY=replace-with-a-local-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1200
```

The application reads the individual `DATABASE_*` settings; it does not use `DATABASE_URL`.

Apply the database migrations and start the development server:

```bash
alembic upgrade head
fastapi dev app/main.py --host 0.0.0.0 --port 8000
```

Run these commands from the repository root with the virtual environment activated. Leave the server running in that terminal; stop it with `Ctrl+C`.

The API is available at `http://localhost:8000`; interactive API docs are at `http://localhost:8000/docs`.

## Development

When changing database models, generate a migration and review the generated file before applying it:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Run the test suite as described in [Test](#test). Tests use a dedicated database and recreate its tables, so do not configure them to use a database containing data you need to retain.

## Build and run with Docker

Build the application image:

```bash
docker build -t org_based_role_system .
```

To run the image, provide the same environment variables shown above in `.env`. The database hostname must be reachable from inside the container (for example, use `host.docker.internal` when the database runs on your Mac):

```bash
docker run --rm --env-file .env -p 8000:8000 org_based_role_system
```

Apply migrations against the same database before starting the container. The API is then available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## Test

Tests use PostgreSQL, not an in-memory database. With the local settings above, create the dedicated test database:

```bash
createdb -h localhost -p 5432 -U postgres test_occam
```

Then run the test suite from the repository root:

```bash
pytest
```

The test fixtures drop and recreate tables in the configured `test_<DATABASE_NAME>` database. Keep that database dedicated to tests; never point the test configuration at a database containing data you need to retain.