# Authentication module

Implementa login con username o email, verificación Argon2 y access tokens JWT.
`GET /api/v1/auth/me` resuelve la identidad activa junto con roles y permisos.

Se usa `HTTPBearer(auto_error=False)` porque el contrato recibe tokens Bearer y
PIA necesita responder 401 de forma uniforme ante header ausente, esquema
incorrecto, token inválido o expirado. El módulo expone dependencias reutilizables
para usuario activo, superusuario y permisos granulares.

No existen refresh tokens, sesiones persistentes, recuperación de contraseña,
2FA ni proveedores OAuth externos en este sprint.

