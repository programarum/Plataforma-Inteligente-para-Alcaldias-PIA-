# ADR-0006: Backend Foundation

- Status: Accepted
- Date: 2026-07-01

## Context

Tras crear la estructura del repositorio, PIA necesita una aplicación backend
funcional que permita desarrollar el Kernel Core de manera incremental. La base
debe mantener bajo acoplamiento, configuración reproducible y límites claros,
sin anticipar lógica de negocio ni autenticación.

## Decision

Se implementará `apps/api` como un monolito modular basado en FastAPI y Python
3.12/3.13. La composición HTTP estará versionada bajo `/api/v1`; la
infraestructura transversal vivirá en `core`; los contratos reutilizables, en
`shared`; y los futuros dominios se aislarán en `modules`.

La configuración se validará con Pydantic Settings. SQLAlchemy 2 y Psycopg 3
proveerán acceso síncrono a PostgreSQL, mientras Alembic administrará futuras
migraciones. Docker Compose ejecutará la API junto con PostgreSQL y uv gestionará
dependencias y comandos de desarrollo.

## Consequences

- Existe una API ejecutable, documentada y verificable desde el Sprint 2.
- El arranque no depende de que existan modelos o migraciones de tablas.
- Los módulos futuros disponen de límites definidos sin capas artificiales.
- La configuración funciona tanto en desarrollo local como en contenedores.
- El equipo debe mantener las dependencias dirigidas hacia los límites internos
  y evitar introducir lógica de negocio en `main.py` o en la infraestructura.

