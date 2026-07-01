"""Users and RBAC API integration tests."""

from fastapi.testclient import TestClient

from app.core.security import hash_password, verify_password


def create_institution(client: TestClient) -> tuple[str, str]:
    municipality = client.post(
        "/api/v1/municipalities",
        json={
            "name": "Alcaldía RBAC",
            "department": "Cundinamarca",
            "country": "Colombia",
            "mayor_name": "Ana Torres",
            "government_period": "2024-2027",
            "mission": "Servicio seguro.",
            "vision": "Institución confiable.",
        },
    ).json()
    department = client.post(
        "/api/v1/departments",
        json={
            "municipality_id": municipality["id"],
            "name": "Tecnología",
            "description": "Gestiona plataformas.",
            "manager_name": "Carlos Ruiz",
        },
    ).json()
    return municipality["id"], department["id"]


def test_password_hash_utility() -> None:
    password = "A-secure-password-123"
    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2")
    assert verify_password(password, password_hash)


def test_user_role_permission_crud_and_assignments(client: TestClient) -> None:
    municipality_id, department_id = create_institution(client)
    user_response = client.post(
        "/api/v1/users",
        json={
            "municipality_id": municipality_id,
            "department_id": department_id,
            "full_name": "Laura Gómez",
            "email": "LAURA@example.gov.co",
            "username": "Laura.Gomez",
            "password": "A-secure-password-123",
            "phone": "3000000000",
            "position": "Administradora",
        },
    )
    assert user_response.status_code == 201
    user = user_response.json()
    assert user["email"] == "laura@example.gov.co"
    assert user["username"] == "laura.gomez"
    assert "password" not in user_response.text
    assert client.get(f"/api/v1/users/{user['id']}").status_code == 200

    role = client.post(
        "/api/v1/roles",
        json={
            "municipality_id": municipality_id,
            "name": "Administrador documental",
            "description": "Gestiona documentos institucionales.",
        },
    ).json()
    permission = client.post(
        "/api/v1/permissions",
        json={
            "code": "DOCUMENTS.WRITE",
            "name": "Gestionar documentos",
            "description": "Permite crear y actualizar documentos.",
            "module": "documents",
            "action": "write",
        },
    ).json()
    assert permission["code"] == "documents.write"

    user_role = client.post(
        f"/api/v1/users/{user['id']}/roles", json={"role_id": role["id"]}
    )
    assert user_role.status_code == 201
    assert client.get(f"/api/v1/users/{user['id']}/roles").json() == [role]

    role_permission = client.post(
        f"/api/v1/roles/{role['id']}/permissions",
        json={"permission_id": permission["id"]},
    )
    assert role_permission.status_code == 201
    assert client.get(f"/api/v1/roles/{role['id']}/permissions").json() == [
        permission
    ]

    assert client.patch(
        f"/api/v1/users/{user['id']}", json={"position": "Líder de TI"}
    ).status_code == 200
    assert client.patch(f"/api/v1/users/{user['id']}/deactivate").json()[
        "is_active"
    ] is False
    assert client.patch(f"/api/v1/roles/{role['id']}/deactivate").json()[
        "is_active"
    ] is False
    assert client.patch(
        f"/api/v1/permissions/{permission['id']}/deactivate"
    ).json()["is_active"] is False

    assert client.delete(
        f"/api/v1/users/{user['id']}/roles/{role['id']}"
    ).status_code == 204
    assert client.delete(
        f"/api/v1/roles/{role['id']}/permissions/{permission['id']}"
    ).status_code == 204


def test_user_and_permission_uniqueness(client: TestClient) -> None:
    municipality_id, _ = create_institution(client)
    payload = {
        "municipality_id": municipality_id,
        "full_name": "Usuario Único",
        "email": "unique@example.gov.co",
        "username": "unique.user",
        "password": "A-secure-password-123",
    }
    assert client.post("/api/v1/users", json=payload).status_code == 201
    assert client.post("/api/v1/users", json=payload).status_code == 409

    permission = {
        "code": "users.read",
        "name": "Consultar usuarios",
        "description": "Permite consultar usuarios.",
        "module": "users",
        "action": "read",
    }
    assert client.post("/api/v1/permissions", json=permission).status_code == 201
    assert client.post("/api/v1/permissions", json=permission).status_code == 409

