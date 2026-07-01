# ADR-0006: Establecer la fundacion del backend

- Estado: Accepted
- Fecha: 2026-07-01

## Contexto

PIA necesita una primera aplicacion backend ejecutable que respete las decisiones de monolito modular, FastAPI y PostgreSQL. La fundacion debe permitir agregar el Kernel Core en el siguiente sprint sin anticipar reglas de negocio, autenticacion o modelos de datos.

## Decision

Crear la API en `apps/api` con Python 3.12, FastAPI, Pydantic v2, pydantic-settings, SQLAlchemy 2, Alembic y PostgreSQL. La estructura separa:

- Entrega HTTP versionada en `app/api`.
- Configuracion e infraestructura transversal en `app/core`.
- Primitivas tecnicas compartidas en `app/shared`.
- Futuros modulos de negocio en `app/modules`.

Pytest verifica el comportamiento HTTP. Ruff y Mypy controlan calidad y tipos. uv gestiona el entorno y Docker Compose proporciona API y PostgreSQL para desarrollo.

No se crean modelos, migraciones de tablas, autenticacion ni modulos funcionales en esta etapa.

## Consecuencias

- Existe una API funcional con contratos iniciales de salud y version.
- El backend puede crecer por modulos sin concentrar logica en `main.py`.
- La configuracion y la sesion de base de datos tienen puntos de acceso consistentes.
- El equipo debe preservar las dependencias hacia adentro al incorporar dominio y casos de uso.
- Los cambios de esquema futuros deben registrarse mediante Alembic.

## Alternativas consideradas

- Extender el directorio historico `backend`: descartado porque la estructura aprobada ubica aplicaciones desplegables en `apps`.
- Crear capas `controllers`, `services` y `repositories`: descartado porque no corresponde a la estructura modular aprobada.
- Implementar modulos de negocio durante la fundacion: descartado para mantener el alcance del sprint.
