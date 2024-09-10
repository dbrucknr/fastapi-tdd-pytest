To visit Adminer: `http://localhost:8080/`

- Use login credentials defined in docker-compose.yml

Initialize Alembic
(Async Alembic References): https://testdriven.io/blog/fastapi-sqlmodel/

- https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
- `alembic init -t async src/database/migrations`
- Migrations are saved in `src/database/migrations/versions`
- For the devdb migrations: `alembic -n devdb revision --autogenerate -m "initial"`
- then: `alembic -n devdb upgrade head`

Pytest: `pytest -s`

## Programmatically Generating Postgres DB with Docker

- Users must have docker downloaded
- `docker ps -a` can be helpful for seeing what containers are up if the context is set to `default` instead of `docker-linux`.
- To switch contexts:
  - `docker context ls`
  - `docker context use default` or `docker context use desktop-linux`
- The programmatically launched database is currently set to be deleted after the Pytest session: `await container.delete(force=True)`
