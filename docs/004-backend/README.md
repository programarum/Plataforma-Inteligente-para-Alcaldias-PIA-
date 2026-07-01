# Backend Foundation

El backend de PIA vive en `apps/api` y se implementa con FastAPI sobre Python 3.12. Su organizacion prepara un monolito modular con separacion inspirada en Clean Architecture, sin introducir todavia modulos o reglas de negocio.

## Estructura inicial

- `app/main.py`: fabrica y ensambla la aplicacion FastAPI.
- `app/api/v1`: composicion de rutas y endpoints HTTP versionados.
- `app/core`: configuracion, base de datos, logging, seguridad y ciclo de vida.
- `app/modules`: limite para futuros modulos de negocio.
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
