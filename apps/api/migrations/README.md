# Migrations

Alembic migrations for the API. Run inside the api container:

```bash
make migrate                      # alembic upgrade head
docker compose run --rm api alembic revision --autogenerate -m "msg"
docker compose run --rm api alembic downgrade -1
```

`env.py` reads `DATABASE_URL` from app settings and targets `app.db.base.Base.metadata`.
