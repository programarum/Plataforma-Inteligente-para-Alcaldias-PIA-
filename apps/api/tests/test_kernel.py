"""Integration tests for the initial Kernel Core modules."""

from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def create_municipality(client: TestClient) -> dict[str, object]:
    """Create and return a municipality through the public API."""
    response = client.post(
        "/api/v1/municipalities",
        json={
            "name": "Alcaldia de Villa Nueva",
            "department": "Cundinamarca",
            "country": "Colombia",
            "mayor_name": "Ana Perez",
            "government_period": "2024-2027",
            "mission": "Servir a la ciudadania",
            "vision": "Un municipio sostenible",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_municipality_crud_flow(client: TestClient) -> None:
    """Municipalities support create, list, get, update, and deactivate."""
    municipality = create_municipality(client)
    municipality_id = municipality["id"]

    list_response = client.get("/api/v1/municipalities")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/api/v1/municipalities/{municipality_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Alcaldia de Villa Nueva"

    update_response = client.patch(
        f"/api/v1/municipalities/{municipality_id}",
        json={"mayor_name": "Carlos Ruiz", "mission": None},
    )
    assert update_response.status_code == 200
    assert update_response.json()["mayor_name"] == "Carlos Ruiz"
    assert update_response.json()["mission"] is None

    deactivate_response = client.patch(
        f"/api/v1/municipalities/{municipality_id}/deactivate"
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["is_active"] is False


def test_department_crud_flow(client: TestClient) -> None:
    """Departments support CRUD operations for an existing municipality."""
    municipality = create_municipality(client)
    response = client.post(
        "/api/v1/departments",
        json={
            "municipality_id": municipality["id"],
            "name": "Secretaria de Planeacion",
            "description": "Planeacion institucional",
            "manager_name": "Laura Gomez",
        },
    )
    assert response.status_code == 201
    department_id = response.json()["id"]

    assert client.get("/api/v1/departments").status_code == 200
    assert client.get(f"/api/v1/departments/{department_id}").status_code == 200

    update_response = client.patch(
        f"/api/v1/departments/{department_id}",
        json={"manager_name": "Diego Torres"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["manager_name"] == "Diego Torres"

    deactivate_response = client.patch(f"/api/v1/departments/{department_id}/deactivate")
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["is_active"] is False


def test_department_requires_existing_municipality(client: TestClient) -> None:
    """A department cannot reference a municipality that does not exist."""
    response = client.post(
        "/api/v1/departments",
        json={"municipality_id": str(uuid4()), "name": "Hacienda"},
    )

    assert response.status_code == 404


def test_audit_repository_persists_records(db_session: Session) -> None:
    """The audit repository stores and returns immutable records."""
    from app.modules.audit.domain.entities import AuditLog
    from app.modules.audit.infrastructure.repositories import SqlAlchemyAuditLogRepository

    repository = SqlAlchemyAuditLogRepository(db_session)
    audit_log = AuditLog(
        actor_id=uuid4(),
        action="municipality.created",
        entity_type="municipality",
        entity_id=uuid4(),
        metadata={"source": "test"},
    )

    persisted = repository.add(audit_log)

    assert persisted.id == audit_log.id
    assert repository.list() == [persisted]
