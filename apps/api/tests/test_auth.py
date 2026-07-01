"""Authentication and reusable authorization dependency tests."""

from typing import Annotated

from fastapi import Depends
from fastapi.testclient import TestClient

from app.main import app
from app.modules.auth.api.dependencies import require_permission
from app.modules.auth.domain.entities import AuthenticatedIdentity


@app.get("/api/v1/test/allowed")
def permission_allowed(
    _: Annotated[
        AuthenticatedIdentity, Depends(require_permission("documents.read"))
    ],
) -> dict[str, bool]:
    return {"allowed": True}


@app.get("/api/v1/test/denied")
def permission_denied(
    _: Annotated[
        AuthenticatedIdentity, Depends(require_permission("documents.delete"))
    ],
) -> dict[str, bool]:
    return {"allowed": True}


def create_identity(client: TestClient, *, active: bool = True) -> dict[str, object]:
    municipality = client.post(
        "/api/v1/municipalities",
        json={
            "name": "Alcaldía Auth",
            "department": "Cundinamarca",
            "country": "Colombia",
            "mayor_name": "Ana Torres",
            "government_period": "2024-2027",
            "mission": "Autenticar con seguridad.",
            "vision": "Acceso confiable.",
        },
    ).json()
    user = client.post(
        "/api/v1/users",
        json={
            "municipality_id": municipality["id"],
            "full_name": "Laura Autenticada",
            "email": "laura.auth@example.gov.co",
            "username": "laura.auth",
            "password": "A-secure-password-123",
        },
    ).json()
    role = client.post(
        "/api/v1/roles",
        json={
            "municipality_id": municipality["id"],
            "name": "Lector documental",
            "description": "Consulta documentos.",
        },
    ).json()
    permission = client.post(
        "/api/v1/permissions",
        json={
            "code": "documents.read",
            "name": "Consultar documentos",
            "description": "Permite consultar documentos.",
            "module": "documents",
            "action": "read",
        },
    ).json()
    client.post(f"/api/v1/users/{user['id']}/roles", json={"role_id": role["id"]})
    client.post(
        f"/api/v1/roles/{role['id']}/permissions",
        json={"permission_id": permission["id"]},
    )
    if not active:
        client.patch(f"/api/v1/users/{user['id']}/deactivate")
    return user


def login(client: TestClient, password: str = "A-secure-password-123") -> object:
    return client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "laura.auth", "password": password},
    )


def test_successful_login_and_me(client: TestClient) -> None:
    create_identity(client)
    response = login(client)
    assert response.status_code == 200
    token = response.json()
    assert token["token_type"] == "bearer"
    assert token["expires_in"] == 3600

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    assert me.status_code == 200
    body = me.json()
    assert body["username"] == "laura.auth"
    assert body["roles"] == ["Lector documental"]
    assert body["permissions"] == ["documents.read"]
    assert "password" not in me.text


def test_login_failures(client: TestClient) -> None:
    create_identity(client)
    assert login(client, "incorrect-password").status_code == 401
    missing = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "nobody", "password": "irrelevant"},
    )
    assert missing.status_code == 401


def test_inactive_user_cannot_login(client: TestClient) -> None:
    create_identity(client, active=False)
    assert login(client).status_code == 401


def test_me_rejects_missing_and_invalid_tokens(client: TestClient) -> None:
    assert client.get("/api/v1/auth/me").status_code == 401
    invalid = client.get(
        "/api/v1/auth/me", headers={"Authorization": "Bearer invalid-token"}
    )
    assert invalid.status_code == 401


def test_require_permission_allows_and_denies(client: TestClient) -> None:
    create_identity(client)
    token = login(client).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get("/api/v1/test/allowed", headers=headers).status_code == 200
    assert client.get("/api/v1/test/denied", headers=headers).status_code == 403

