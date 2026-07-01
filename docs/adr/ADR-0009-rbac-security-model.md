# ADR-0009: RBAC Security Model

- Status: Accepted
- Date: 2026-07-01

## Context

PIA necesita identidades institucionales y autorización granular antes de
implementar login. El modelo debe respetar el ámbito municipal, evitar almacenar
contraseñas reversibles y permitir evolucionar hacia políticas verificables.

## Decision

Se adopta RBAC con User, Role y Permission. Los roles pertenecen a una alcaldía;
un usuario solo puede recibir roles del mismo municipio. Los permisos tienen un
código global único y se asignan a roles mediante relaciones explícitas.

Las contraseñas se transforman con Argon2 usando `pwdlib`. Solo `password_hash`
se persiste y los contratos HTTP nunca lo exponen. La autenticación, JWT y la
protección de endpoints quedan reservados para el Sprint 6.

## Consequences

- Identidad y autorización evolucionan como capacidades separadas.
- Las asignaciones duplicadas quedan impedidas por reglas y constraints.
- El alcance municipal reduce cruces accidentales entre instituciones.
- Los endpoints permanecen abiertos hasta incorporar autenticación.
- Los futuros checks de autorización podrán resolver permisos vía roles.

