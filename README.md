To visit Adminer: `http://localhost:8080/`

- Use login credentials defined in docker-compose.yml

Initialize Alembic
(Async Alembic References): https://testdriven.io/blog/fastapi-sqlmodel/

- https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
- `alembic init -t async src/database/migrations`
- Migrations are saved in `src/database/migrations/versions`
- For the devdb migrations: `alembic -n devdb revision --autogenerate -m "initial"`
