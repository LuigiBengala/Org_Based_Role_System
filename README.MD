# OCCAM Home Assignment

> **Note:** .env.example is only equal to the .env to facilitate the testing. Create a .env file and copy and paste everything from the .env.example
> **Note:** You can always access "localhost:8000/docs" or "localhost:8000/redocs" for the built-in fastapi documentation

# Run the API

## Using Docker

Use the Docker build to create the image:

```bash
docker build -t 'occamassigment:latest' .
```

Use the docker run to create and start the container:

```bash
docker run --env-file .env occamassigment:latest
```

## Using Fast api built-in tools

(Optional): Use the following command to create a virtual environment:
```bash
python -m venv env
```

(optional): Use the following command to use the virtual environment:
```bash
#On mac/linux
source myvenv/bin/activate

#On Windows
env\Scripts\activate
```

Use the following command to install the packages needed to run the api:
```bash
pip install -r requirements.txt
```

Use the built-in FastAPI command to run the api:
```bash
fastapi run ./app/main.py
```

# Testing

## Fast API docs

You can use the built-in FastAPI docs to test the api.

## Postman

If you want to use Postman to test the api, you can find the collection file in the project folder.


# Architecture and Design Choices

## Architectures

- **FastAPI** with modular router structure
- **SQLAlchemyORM** with SQLite for development and testing simplicity
- **Pydantic Schemas** for request/response validation and serialisation
- **JWT-based authentication** with role-based access control

## Design Choices

**Modular Router**
- Separated endpoints into logical modules: user.py, organization.py, study.py, session.py, auth.py;
- Each router handles its own domain.

**Role-Based Access Control**

- Implemented org-scoped permissions with 4 roles: Admin, Study Coordinator, Research Assistant, Participant;

- Org-level isolation: Users can only access data within their organisation

- Graduated permissions: Each role has specific access patterns

**DataBase**

- Foreign key constraints are enabled to ensure referential integrity

- Enum-based roles stored as strings for database compatibility

- Nullable org field for admin users who exist before organisations are created

**Security and Validation**

- JWT tokens with configurable expiration

- Password hashing using bcrypt

- Pydantic validation for all input/output data

- Database seeding for initial admin user creation

**Development**

- Environment-based configuration using .env files

- Docker support for consistent deployment

- Modular utility functions for reusable business logic (role checking, password hashing)
