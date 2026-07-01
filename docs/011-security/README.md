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

## JWT authentication

El Sprint 6 verifica contraseñas Argon2 y emite access tokens JWT HS256 con
subject de usuario, fecha de emisión y expiración configurable. La clave,
algoritmo y duración se obtienen exclusivamente del entorno.

`HTTPBearer` extrae credenciales sin respuestas automáticas para mantener un
contrato 401 uniforme. La identidad se vuelve a consultar en cada solicitud, por
lo que usuarios desactivados dejan de acceder aunque conserven un token vigente.
Las dependencias `require_superuser` y `require_permission` producen 403 cuando
la identidad autenticada carece del grant; superusuarios omiten checks RBAC.

No se persisten sesiones ni refresh tokens y aún no existen recuperación de
contraseña, 2FA u OAuth externo.
