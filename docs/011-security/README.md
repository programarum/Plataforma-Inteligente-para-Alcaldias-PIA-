# Security

## RBAC foundation

PIA separa identidad, agrupación de responsabilidades y acciones granulares:

- Users identifica funcionarios y administradores institucionales.
- Roles agrupa permisos dentro de una alcaldía.
- Permissions define acciones mediante códigos únicos como `documents.write`.
- UserRole y RolePermission materializan las asignaciones.

Las contraseñas se reciben únicamente al crear una identidad y se transforman
con Argon2 mediante `pwdlib`. Solo el hash se persiste y nunca forma parte de las
respuestas HTTP. Emails, usernames y códigos de permiso son únicos.

Esta fase no autentica solicitudes, no emite JWT y no protege endpoints. El
Sprint 6 deberá verificar hashes, emitir credenciales y evaluar RBAC sin mover
estas reglas a los routers.

