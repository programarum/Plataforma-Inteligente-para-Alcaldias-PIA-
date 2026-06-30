# ADR-0004: Usar PostgreSQL como base de datos

- Estado: Accepted
- Fecha: 2026-06-30

## Contexto

PIA gestionara informacion institucional que requiere integridad, consultas consistentes, transacciones y mecanismos maduros de operacion y respaldo.

## Decision

Usar PostgreSQL como sistema principal de persistencia relacional. En el monolito modular, cada modulo mantendra propiedad logica sobre sus datos aunque comparta la misma instancia de base de datos.

Los esquemas, migraciones y politicas operativas se definiran en sprints posteriores.

## Consecuencias

- Transacciones ACID e integridad referencial.
- Herramientas maduras para respaldo, monitoreo y recuperacion.
- Se requiere gobernar migraciones y acceso entre modulos.
- Las capacidades especificas de otros motores necesitaran justificacion independiente.

## Alternativas consideradas

- Bases de datos documentales como persistencia principal: rechazadas porque no ofrecen una ventaja inicial frente al modelo relacional previsto.
- Una base independiente por modulo: rechazada por complejidad operativa prematura.
