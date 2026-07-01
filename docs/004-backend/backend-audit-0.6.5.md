# Auditoría técnica del backend 0.6.5

- Fecha: 2026-07-01
- Alcance: backend FastAPI hasta autenticación JWT
- Resultado: estable y preparado para iniciar el Sprint 7

## Estado general

El backend mantiene un monolito modular coherente. Los endpoints delegan en
casos de uso, la persistencia permanece dentro de cada módulo y no existen capas
globales `controllers`, `services` o `repositories`. La cadena de migraciones,
los contratos HTTP, JWT y RBAC fueron verificados localmente y en PostgreSQL.

Resultados finales:

- Pytest: 17 pruebas superadas.
- Ruff: sin hallazgos.
- Mypy: 131 archivos sin errores.
- Docker Compose: API y PostgreSQL saludables.
- Alembic: upgrade, check y downgrade correctos desde una base vacía.
- Git: sin caches, entornos virtuales, bases SQLite ni archivos `.env` rastreados.

## Módulos revisados

Se revisaron `municipalities`, `departments`, `audit`, `documents`, `knowledge`,
`users`, `roles`, `permissions` y `auth`. Todos contienen `api`, `application`,
`domain`, `infrastructure`, `tests` y `README.md`.

Los nombres de código están en inglés y la documentación explicativa está en
español. Los routers se limitan a transporte, validación de schemas y composición
de dependencias; las reglas permanecen en servicios de aplicación.

## SQLAlchemy y Alembic

Se encontraron 12 modelos y 12 tablas con nombres plurales coherentes. Todos los
identificadores primarios son UUID. Las entidades mutables incluyen `created_at`
y `updated_at` con timestamps UTC.

`AuditLog`, `DocumentChunk`, `KnowledgeRelation`, `UserRole` y `RolePermission`
son registros append-only y conservan únicamente `created_at` de forma
intencional. Sus relaciones se protegen mediante claves foráneas, constraints e
índices; no se añadieron propiedades ORM de navegación sin un caso de uso real.

Las migraciones `0001`, `0002` y `0003` forman una única cadena ordenada. El
entorno Alembic importa explícitamente todos los modelos, incluido `AuditLog`, y
`alembic check` no detectó operaciones pendientes.

## Pydantic y seguridad

Los recursos mutables separan schemas de creación, actualización y respuesta.
Las asignaciones y autenticación utilizan contratos específicos. Ningún schema
de salida contiene `password`, `password_hash`, JWT secret u otro dato sensible.

Los passwords se almacenan con Argon2. JWT obtiene secreto, algoritmo y duración
desde settings ambientales, valida firma y expiración, y resuelve nuevamente el
usuario activo. `require_permission` es parametrizable y reutilizable; los
superusuarios omiten únicamente la decisión de permiso.

## Problemas encontrados

- Faltaban README en Municipality, Department y Audit.
- Gitignore no excluía `*.db` ni `*.sqlite3`.
- Un `DEBUG=release` global del entorno impedía ejecutar comandos locales de
  configuración y Alembic.
- Faltaba una prueba directa de rechazo de JWT expirado.

## Problemas corregidos

- Se completó el contrato documental de los nueve módulos.
- Se añadieron exclusiones para bases locales y se verificó que no existan
  caches rastreados.
- Settings normaliza `debug/development` y `release/production` sin romper
  valores booleanos convencionales.
- Se añadió la prueba mínima de expiración JWT.

## Problemas pendientes

- FastAPI TestClient emite un warning upstream sobre la transición de HTTPX; no
  afecta comportamiento y no se añadió una dependencia innecesaria para ocultarlo.
- Los repositorios confirman transacciones individualmente. Es suficiente para
  CRUD actual, pero la ingestión multi-etapa puede necesitar una unidad de trabajo
  explícita para atomicidad entre documentos, chunks y knowledge items.
- No existe aún política automática de escritura de AuditLog, por decisión de
  alcance previa.

## Recomendaciones antes del Sprint 7

- Diseñar la ingestión como pipeline idempotente con estados y límites de
  transacción explícitos antes de incorporar workers.
- Definir tamaño, orden y deduplicación de chunks sin añadir embeddings todavía.
- Incorporar auditoría de transiciones relevantes del pipeline.
- Mantener Documents como custodia de archivos y Knowledge como frontera de
  consumo futuro para búsqueda o RAG.
- Añadir observabilidad de errores y tiempos del pipeline sin registrar contenido
  sensible ni credenciales.

