# ADR-0007: Introducir el Kernel Core institucional

- Estado: Accepted
- Fecha: 2026-07-01

## Contexto

PIA necesita representar la institucion municipal antes de incorporar identidad, documentos o inteligencia artificial. Estas entidades iniciales deben establecer un lenguaje comun, persistencia auditable y limites modulares compatibles con el monolito modular y Clean Architecture.

## Decision

Crear tres modulos verticales dentro de `apps/api/app/modules`:

- `municipalities`: administra la informacion institucional de cada alcaldia.
- `departments`: administra dependencias organizacionales pertenecientes a una alcaldia.
- `audit`: establece el modelo y repositorio para registros de auditoria.

Cada modulo separa `domain`, `application`, `infrastructure`, `api` y `tests`. Las entidades de dominio son dataclasses independientes. Los contratos de repositorio viven en dominio, los casos de uso dependen de esos contratos y SQLAlchemy implementa la persistencia en infraestructura. Los routers solo adaptan HTTP hacia los casos de uso.

Los identificadores son UUID y las marcas temporales son conscientes de zona horaria y se generan en UTC. La desactivacion es logica; no se ofrece eliminacion fisica. `Department` requiere una `Municipality` existente. `AuditLog` no tiene API ni automatizacion en esta etapa.

## Consecuencias

- El backend dispone de su primer modelo institucional funcional.
- Los modulos pueden evolucionar con responsabilidades y dependencias explicitas.
- Las APIs de alcaldias y dependencias comparten convenciones CRUD consistentes.
- La conversion entre entidades de dominio y modelos ORM agrega codigo, pero evita acoplar los casos de uso a SQLAlchemy.
- La integracion futura de auditoria debera definir actores y eventos sin introducir usuarios anticipadamente.

## Alternativas consideradas

- Usar modelos SQLAlchemy directamente como entidades de dominio: descartado porque acopla reglas y casos de uso a persistencia.
- Crear repositorios o servicios globales: descartado porque rompe la propiedad modular.
- Eliminar registros fisicamente: descartado para preservar trazabilidad institucional.
- Implementar autenticacion junto al Kernel Core: descartado por estar fuera del alcance del sprint.
