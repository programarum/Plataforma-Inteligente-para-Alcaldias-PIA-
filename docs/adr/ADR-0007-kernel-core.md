# ADR-0007: Institutional Kernel Core

- Status: Accepted
- Date: 2026-07-01

## Context

PIA necesita representar la estructura institucional mínima de una alcaldía
antes de incorporar usuarios, autenticación o capacidades funcionales. Estas
entidades deben crecer dentro del monolito modular sin acoplar reglas de negocio
al transporte HTTP ni crear repositorios globales.

## Decision

Se crean tres módulos: `municipalities`, `departments` y `audit`. Cada módulo
separa `api`, `application`, `domain`, `infrastructure` y `tests`.

Municipality es la raíz institucional inicial. Department pertenece a una
Municipality existente mediante clave foránea restrictiva. Ambas entidades
ofrecen CRUD mínimo con desactivación lógica. AuditLog se incorpora como modelo
append-only y repositorio, sin API ni integración automática hasta definir el
actor en un sprint futuro.

Los modelos usan UUID, timestamps con zona horaria y SQLAlchemy 2. Pydantic v2
valida los límites HTTP. Los casos de uso dependen de puertos de repositorio y
los adaptadores SQLAlchemy administran persistencia y transacciones. Alembic
versiona el esquema PostgreSQL.

## Consequences

- PIA puede registrar alcaldías y su estructura organizacional básica.
- La desactivación conserva referencias y trazabilidad histórica.
- Los módulos futuros pueden consumir contratos institucionales definidos.
- AuditLog queda preparado, pero no registra acciones hasta contar con una
  política explícita de auditoría y actores.
- No se introducen usuarios, autenticación, JWT ni autorización en este sprint.

