# ADR-0011: Backend Stabilization Before Ingestion

- Status: Accepted
- Date: 2026-07-01

## Context

Antes de introducir ingestión documental, PIA necesita una base verificable y
criterios claros para no convertir el nuevo pipeline en un refactor transversal.

## Decision

Se mantiene la estructura modular uniforme y se formaliza que las entidades
mutables tienen timestamps de creación y actualización, mientras los registros
append-only conservan solo creación. Las relaciones se expresan con constraints
y repositorios hasta que exista una necesidad concreta de navegación ORM.

La configuración ambiental tolerará nombres de modo comunes del entorno de
desarrollo, manteniendo validación estricta para el resto. La ingestión futura
deberá evaluar una unidad de trabajo explícita si una operación modifica varios
agregados.

## Consequences

- El Sprint 7 puede concentrarse en ingestión sin reorganizar el backend.
- Las excepciones de timestamps quedan documentadas y no generan migraciones
  artificiales.
- Se evita añadir abstracciones transaccionales antes de conocer el pipeline.
- La calidad actual queda respaldada por pruebas, tipado y Alembic check.

