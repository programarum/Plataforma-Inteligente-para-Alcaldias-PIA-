# Backend

El backend inicial de PIA vive en `apps/api` y sigue un monolito modular con
separación de responsabilidades inspirada en Clean Architecture. El Sprint 2
establece únicamente la infraestructura técnica; los módulos de negocio se
incorporarán en sprints posteriores.

## Estructura inicial

```text
apps/api/
├── app/
│   ├── api/v1/       # Composición HTTP y endpoints versionados
│   ├── core/         # Configuración e infraestructura transversal
│   ├── modules/      # Límite reservado para módulos de negocio
│   └── shared/       # Contratos y excepciones compartidas
├── alembic/          # Entorno de migraciones de base de datos
├── tests/            # Pruebas de comportamiento de la API
├── Dockerfile
└── pyproject.toml
```

`app/main.py` solo compone la aplicación. Los routers gestionan el transporte
HTTP; `core` concentra configuración, logging, ciclo de vida y acceso a base de
datos. `modules` contiene límites funcionales independientes.

## Kernel Core

Los módulos `municipalities`, `departments` y `audit` siguen la misma estructura:

```text
<module>/
├── api/             # Routers y contratos Pydantic
├── application/     # Comandos y casos de uso
├── domain/          # Entidades y puertos de repositorio
├── infrastructure/  # Adaptadores SQLAlchemy
└── tests/           # Límite de pruebas del módulo
```

Municipalities y Departments exponen creación, listado, consulta, actualización
y desactivación bajo `/api/v1`. Audit incorpora únicamente su modelo y
repositorio; todavía no expone endpoints. Los casos de uso dependen de contratos
de repositorio y los routers no contienen reglas institucionales.

## Decisiones técnicas

- FastAPI y Pydantic v2 para API y contratos tipados.
- `pydantic-settings` para configuración por variables de entorno.
- SQLAlchemy 2 con sesiones síncronas y el driver Psycopg 3.
- Alembic conectado al mismo metadata, sin migraciones iniciales de tablas.
- PostgreSQL y API ejecutables mediante Docker Compose.
- Pytest, Ruff y Mypy como controles locales de calidad.

Los endpoints de sistema `/api/v1/health` y `/api/v1/version` se mantienen sin
cambios. No existen aún autenticación, usuarios, roles, documentos ni
componentes de inteligencia artificial.

La primera migración Alembic crea `municipalities`, `departments` y `audit_logs`.
El contenedor API ejecuta `alembic upgrade head` antes de iniciar el servidor.

