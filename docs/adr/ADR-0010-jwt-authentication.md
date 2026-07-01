# ADR-0010: JWT Authentication

- Status: Accepted
- Date: 2026-07-01

## Context

PIA dispone de usuarios y RBAC, pero necesita autenticar solicitudes sin añadir
sesiones persistentes, refresh tokens ni infraestructura de identidad externa.

## Decision

Se emitirán access tokens JWT firmados con algoritmo y secreto configurables.
El subject será el UUID del usuario; cada solicitud volverá a cargar la identidad
activa y sus grants para respetar desactivaciones y cambios RBAC.

Se adopta `HTTPBearer(auto_error=False)` en lugar de OAuth2PasswordBearer porque
el login usa un cuerpo JSON propio (`username_or_email` y `password`) y no el
formulario OAuth2. Desactivar el error automático permite responder siempre 401
con `WWW-Authenticate: Bearer` ante credenciales ausentes o inválidas.

## Consequences

- La API puede autenticar usuarios y exponer su contexto RBAC.
- No se almacena estado de sesión en el servidor.
- Cambios de usuario o permisos se reflejan al resolver cada solicitud.
- Revocación individual, refresh tokens, 2FA y OAuth quedan pendientes.
- Los secretos deben suministrarse por entorno y rotarse operacionalmente.

