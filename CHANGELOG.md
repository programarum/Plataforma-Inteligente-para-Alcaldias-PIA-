# Changelog

Todos los cambios relevantes de PIA se documentan en este archivo. El formato se basa en Keep a Changelog y el proyecto utiliza versionado semantico.

## [Unreleased]

## [0.3.0] - 2026-07-01

### Added

- Modulos verticales para alcaldias, dependencias organizacionales y auditoria.
- Entidades de dominio y modelos SQLAlchemy con UUID y timestamps UTC.
- Repositorios y casos de uso basicos por modulo.
- Endpoints CRUD de alcaldias y dependencias con desactivacion logica.
- Migracion Alembic inicial del Kernel Core.
- Pruebas integradas para APIs y persistencia de auditoria.
- Documentacion de dominio, backend y ADR-0007.

## [0.2.0] - 2026-07-01

### Added

- Aplicacion backend inicial con FastAPI y endpoints de salud y version.
- Configuracion tipada mediante pydantic-settings.
- Fundacion de persistencia con SQLAlchemy 2, PostgreSQL y Alembic.
- Pruebas con Pytest y validaciones con Ruff y Mypy.
- Entorno Docker Compose para API y PostgreSQL.
- Documentacion de la fundacion backend y ADR-0006.

## [0.1.0] - 2026-06-30

### Added

- Estructura base para aplicaciones, paquetes, infraestructura, pruebas y herramientas.
- Documentacion inicial de vision, negocio, dominio y arquitectura.
- Registros iniciales de decisiones arquitectonicas.
- Plantillas de issues y pull requests.
- Validacion continua de la estructura del repositorio.

[Unreleased]: https://github.com/example/pia/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/example/pia/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/example/pia/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/example/pia/releases/tag/v0.1.0
