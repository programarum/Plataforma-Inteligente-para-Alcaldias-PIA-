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
datos. `modules` permanece vacío para evitar anticipar el Kernel Core.

## Decisiones técnicas

- FastAPI y Pydantic v2 para API y contratos tipados.
- `pydantic-settings` para configuración por variables de entorno.
- SQLAlchemy 2 con sesiones síncronas y el driver Psycopg 3.
- Alembic conectado al mismo metadata, sin migraciones iniciales de tablas.
- PostgreSQL y API ejecutables mediante Docker Compose.
- Pytest, Ruff y Mypy como controles locales de calidad.

Los endpoints iniciales son `/api/v1/health` y `/api/v1/version`. No existen aún
autenticación, usuarios, roles, documentos, módulos funcionales ni componentes
de inteligencia artificial.

