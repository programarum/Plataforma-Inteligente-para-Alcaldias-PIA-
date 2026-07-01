# Audit

Define el registro append-only `AuditLog` y su repositorio. No expone endpoints
ni automatiza eventos todavía. Por su carácter inmutable conserva `created_at`
pero no `updated_at`; la política integral de auditoría queda pendiente.

