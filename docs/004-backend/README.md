# Backend Foundation

El backend de PIA vive en `apps/api` y se implementa con FastAPI sobre Python 3.12. Su organizacion prepara un monolito modular con separacion inspirada en Clean Architecture, sin introducir todavia modulos o reglas de negocio.

## Estructura inicial

- `app/main.py`: fabrica y ensambla la aplicacion FastAPI.
- `app/api/v1`: composicion de rutas y endpoints HTTP versionados.
- `app/core`: configuracion, base de datos, logging, seguridad y ciclo de vida.
- `app/modules`: modulos verticales de negocio con limites propios.
- `app/shared`: excepciones y esquemas tecnicos compartidos.
- `alembic`: entorno para futuras migraciones SQLAlchemy.
- `tests`: pruebas automatizadas de la superficie HTTP.

## Persistencia

SQLAlchemy 2 proporciona el engine, la base declarativa y la fabrica de sesiones. PostgreSQL es la persistencia principal y `psycopg` su driver. No existen modelos ni tablas en esta etapa.

## Configuracion

`pydantic-settings` carga la configuracion desde variables de entorno. Los secretos no se incluyen en el codigo ni deben versionarse en archivos `.env`.

## Operacion

El entorno Docker de la raiz inicia los servicios `postgres` y `api`. La API publica Swagger en `/docs`, salud en `/api/v1/health` y metadata en `/api/v1/version`.

Las instrucciones de ejecucion y validacion se encuentran en el [README de la API](../../apps/api/README.md).

## Kernel Core

Los modulos `municipalities`, `departments` y `audit` siguen la misma estructura interna:

- `domain`: entidades y contratos de repositorio sin dependencias de framework.
- `application`: servicios que coordinan casos de uso.
- `infrastructure`: modelos y repositorios SQLAlchemy.
- `api`: esquemas Pydantic y rutas FastAPI.
- `tests`: limite reservado para pruebas propias del modulo; las pruebas integradas actuales viven en `apps/api/tests`.

`Municipality` y `Department` exponen operaciones para crear, listar, consultar, actualizar y desactivar. `AuditLog` dispone solamente de modelo y repositorio en esta etapa.

## Endpoints del Kernel

- `POST /api/v1/municipalities`
- `GET /api/v1/municipalities`
- `GET /api/v1/municipalities/{municipality_id}`
- `PATCH /api/v1/municipalities/{municipality_id}`
- `PATCH /api/v1/municipalities/{municipality_id}/deactivate`
- `POST /api/v1/departments`
- `GET /api/v1/departments`
- `GET /api/v1/departments/{department_id}`
- `PATCH /api/v1/departments/{department_id}`
- `PATCH /api/v1/departments/{department_id}/deactivate`

La migracion `20260701_0001` crea las tablas `municipalities`, `departments` y `audit_logs`, junto con sus claves e indices iniciales.
