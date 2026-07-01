# PIA API

Backend inicial de PIA construido con FastAPI, Pydantic v2, SQLAlchemy 2 y PostgreSQL. La aplicacion sigue un monolito modular y separa la entrega HTTP de configuracion, infraestructura y futuros modulos de negocio.

## Requisitos

- Python 3.12 o 3.13.
- uv.
- Docker y Docker Compose para ejecutar el entorno completo.

## Ejecucion local

Desde `apps/api`:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000` y Swagger en `http://localhost:8000/docs`.

La configuracion se lee desde variables de entorno y, para desarrollo local, desde un archivo `.env`. Usa `.env.example` como referencia.

## Ejecucion con Docker

Desde la raiz del repositorio:

```bash
docker compose up --build
```

Compose inicia PostgreSQL y la API. Para detenerlos:

```bash
docker compose down
```

## Verificaciones

Desde `apps/api`:

```bash
uv run pytest
uv run ruff check .
uv run mypy app
```

## Endpoints iniciales

- `GET /api/v1/health`: estado del proceso de API.
- `GET /api/v1/version`: version y entorno configurados.
- `/api/v1/municipalities`: creacion, listado, consulta, actualizacion y desactivacion de alcaldias.
- `/api/v1/departments`: creacion, listado, consulta, actualizacion y desactivacion de dependencias.

## Migraciones

Alembic usa `DATABASE_URL` y la metadata declarativa de SQLAlchemy. Desde `apps/api`, aplica las migraciones con:

```bash
uv run alembic upgrade head
```

Con Docker, ejecuta la migracion una vez que los servicios esten activos:

```bash
docker compose exec api .venv/bin/alembic upgrade head
```

La revision `20260701_0001` crea las tablas iniciales del Kernel Core. Toda modificacion futura del esquema debe incorporarse mediante una nueva migracion.
