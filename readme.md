This my current vision of the FastAPI structure.

Short description of this structure and changes:

v.2.0.0 - Unit of Work:
- Added transaction manager to handle the database transactions

v.1.0.0 - Onion Architecture:

- Take beyond the logic from the API endpoints and put it in the middle layer
- Added SQLAlchemy models and linked them with Pydantic schemas through to_read_model
- Changed orm_mode for schemas class Config to from_attributes (for Pydantic v2)
- Added Service layer to handle the logic of the API endpoints
- Added Repository layer to handle the logic of the database (based on dependency inversion principle from SOLID principles)

TODO:

- Add tests
- Add abstract class for choosing DB
- Add PostgreSQL database
- Add logger


1. For autogenerated migration files for updating DB, run (NB! you need to add paths to models to the migrations/env file if you want to autogenerate migration successfully (as this moment I don't know why)):

```
alembic revision --autogenerate -m "description_of_changes"

```

2. For running the migration, run:

```
alembic upgrade head
```

3. For running check of the code, run:

```
ruff check app
```

4. For running the formatting of the code, run:

```
ruff format app
```

5. Before running the project in docker create docker network:

```
docker network create test-fastapi-sql-network
```
6. Run the project in docker:

```
docker-compose up
```