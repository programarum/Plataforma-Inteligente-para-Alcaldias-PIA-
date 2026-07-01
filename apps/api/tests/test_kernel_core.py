"""Kernel Core API integration tests."""

from uuid import uuid4

from fastapi.testclient import TestClient

MUNICIPALITY_PAYLOAD = {
    "name": "Alcaldía de Villa Esperanza",
    "department": "Cundinamarca",
    "country": "Colombia",
    "mayor_name": "Ana Torres",
    "government_period": "2024-2027",
    "mission": "Servir con transparencia.",
    "vision": "Ser un municipio sostenible.",
}


def create_municipality(client: TestClient) -> dict[str, object]:
    response = client.post("/api/v1/municipalities", json=MUNICIPALITY_PAYLOAD)
    assert response.status_code == 201
    return response.json()


def test_municipality_crud(client: TestClient) -> None:
    municipality = create_municipality(client)
    municipality_id = municipality["id"]

    assert municipality["is_active"] is True
    assert client.get("/api/v1/municipalities").json() == [municipality]
    assert client.get(f"/api/v1/municipalities/{municipality_id}").status_code == 200

    updated = client.patch(
        f"/api/v1/municipalities/{municipality_id}",
        json={"mayor_name": "Lucía Gómez"},
    )
    assert updated.status_code == 200
    assert updated.json()["mayor_name"] == "Lucía Gómez"

    deactivated = client.patch(
        f"/api/v1/municipalities/{municipality_id}/deactivate"
    )
    assert deactivated.status_code == 200
    assert deactivated.json()["is_active"] is False


def test_department_crud(client: TestClient) -> None:
    municipality = create_municipality(client)
    payload = {
        "municipality_id": municipality["id"],
        "name": "Secretaría de Planeación",
        "description": "Coordina la planeación institucional.",
        "manager_name": "Carlos Ruiz",
    }
    created = client.post("/api/v1/departments", json=payload)
    assert created.status_code == 201
    department = created.json()
    department_id = department["id"]

    assert client.get("/api/v1/departments").json() == [department]
    assert client.get(f"/api/v1/departments/{department_id}").status_code == 200

    updated = client.patch(
        f"/api/v1/departments/{department_id}",
        json={"manager_name": "María López"},
    )
    assert updated.status_code == 200
    assert updated.json()["manager_name"] == "María López"

    deactivated = client.patch(f"/api/v1/departments/{department_id}/deactivate")
    assert deactivated.status_code == 200
    assert deactivated.json()["is_active"] is False


def test_department_requires_existing_municipality(client: TestClient) -> None:
    response = client.post(
        "/api/v1/departments",
        json={
            "municipality_id": str(uuid4()),
            "name": "Secretaría Jurídica",
            "description": "Asuntos jurídicos.",
            "manager_name": "Laura Díaz",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Municipality not found"}

