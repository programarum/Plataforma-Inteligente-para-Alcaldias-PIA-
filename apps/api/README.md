# PIA API

Base del backend de PIA construida con FastAPI, SQLAlchemy 2 y PostgreSQL.

## Requisitos

- Python 3.12 o 3.13.
- [uv](https://docs.astral.sh/uv/).
- Docker con Docker Compose, para ejecutar el entorno completo.

## Ejecución local

Desde `apps/api`:

```bash
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000` y Swagger en
`http://localhost:8000/docs`.

La URL de base de datos predeterminada usa el hostname `postgres` de Docker. Si
la API se ejecuta directamente en el host, configure `DATABASE_URL` con el host
y puerto de su instancia local de PostgreSQL.

## Ejecución con Docker

Desde la raíz del repositorio:

```bash
docker compose up --build
```

El comando inicia PostgreSQL y la API. Para detenerlos use
`docker compose down`. Los datos de PostgreSQL se conservan en un volumen.

## Endpoints iniciales

- `GET /api/v1/health`: disponibilidad del servicio.
- `GET /api/v1/version`: versión y entorno de la aplicación.
- `GET /docs`: documentación interactiva OpenAPI.

## Calidad

Desde `apps/api`:

```bash
uv run pytest
uv run ruff check .
uv run mypy app
```

## Alembic

Alembic comparte la configuración de conexión de la aplicación. Aún no existen
modelos ni migraciones de tablas. Cuando se incorporen modelos, los comandos se
ejecutarán desde `apps/api`, por ejemplo:

```bash
uv run alembic current
```

