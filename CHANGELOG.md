# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2026-07-01

### Added
- JWT access-token authentication using username or email credentials.
- Current-user endpoint with effective roles and permissions.
- Reusable active-user, superuser and granular permission dependencies.
- Consistent 401 handling for missing, invalid and expired bearer tokens.
- Authentication and authorization integration tests.

## [0.5.0] - 2026-07-01

### Added
- User, role and granular permission modules as the RBAC foundation.
- Argon2 password hashing with no password hashes in API responses.
- User-role and role-permission assignment, listing and removal endpoints.
- Unique identity and permission constraints with institutional role scoping.
- Alembic migration and integration tests for identity and RBAC workflows.

## [0.4.0] - 2026-07-01

### Added
- Document metadata and manually supplied document chunk management.
- Knowledge items and directed relations as the Knowledge Core foundation.
- Modular repositories, use cases and HTTP APIs for documents and knowledge.
- Alembic migration for document and knowledge persistence structures.
- Integration tests covering document, chunk, knowledge item and relation flows.

## [0.3.0] - 2026-07-01

### Added
- Institutional Kernel Core modules for municipalities, departments and audit.
- Municipality and department CRUD APIs with explicit deactivation operations.
- UUID-based SQLAlchemy models with UTC timestamps and modular repositories.
- Initial Alembic migration for Kernel Core tables and constraints.
- Integration tests for institutional API workflows and validation rules.

## [0.2.0] - 2026-07-01

### Added
- FastAPI backend foundation with versioned health and version endpoints.
- Environment configuration, logging, lifespan and SQLAlchemy session setup.
- Alembic migration environment prepared for future models.
- PostgreSQL and API services through Docker Compose.
- Pytest, Ruff and Mypy development quality configuration.
- Backend operation guide and architectural decision record.

## [0.1.0] - 2026-07-01

### Added
- Initial repository foundation.
- Documentation structure for vision, business, domain, architecture and roadmap.
- ADR baseline for architectural decisions.
- Contribution, conduct and pull request templates.
- Initial CI workflow placeholder for repository validation.
