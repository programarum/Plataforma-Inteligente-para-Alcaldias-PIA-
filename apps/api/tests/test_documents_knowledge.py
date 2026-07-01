"""Documents and Knowledge Core API integration tests."""

from fastapi.testclient import TestClient


def create_institution(client: TestClient) -> tuple[str, str]:
    municipality = client.post(
        "/api/v1/municipalities",
        json={
            "name": "Alcaldía del Conocimiento",
            "department": "Cundinamarca",
            "country": "Colombia",
            "mayor_name": "Elena Ruiz",
            "government_period": "2024-2027",
            "mission": "Gestionar conocimiento público.",
            "vision": "Ser una institución informada.",
        },
    ).json()
    department = client.post(
        "/api/v1/departments",
        json={
            "municipality_id": municipality["id"],
            "name": "Gestión Documental",
            "description": "Custodia documentos institucionales.",
            "manager_name": "Mario Solano",
        },
    ).json()
    return municipality["id"], department["id"]


def create_document(client: TestClient) -> dict[str, object]:
    municipality_id, department_id = create_institution(client)
    response = client.post(
        "/api/v1/documents",
        json={
            "title": "Plan de Desarrollo Municipal",
            "description": "Metas institucionales del periodo.",
            "document_type": "plan",
            "source": "Secretaría de Planeación",
            "file_path": "/documents/plan-2024.pdf",
            "file_name": "plan-2024.pdf",
            "file_extension": "pdf",
            "mime_type": "application/pdf",
            "size_bytes": 4096,
            "checksum": "abc123",
            "version": "1.0",
            "confidentiality_level": "public",
            "municipality_id": municipality_id,
            "department_id": department_id,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_document_metadata_and_chunks(client: TestClient) -> None:
    document = create_document(client)
    document_id = document["id"]

    assert client.get("/api/v1/documents").json() == [document]
    assert client.get(f"/api/v1/documents/{document_id}").status_code == 200

    updated = client.patch(
        f"/api/v1/documents/{document_id}", json={"version": "1.1"}
    )
    assert updated.status_code == 200
    assert updated.json()["version"] == "1.1"

    chunk = client.post(
        f"/api/v1/documents/{document_id}/chunks",
        json={
            "chunk_index": 0,
            "content": "Objetivo estratégico institucional.",
            "page_number": 3,
            "metadata": {"section": "objetivos"},
        },
    )
    assert chunk.status_code == 201
    assert chunk.json()["metadata"] == {"section": "objetivos"}
    chunks = client.get(f"/api/v1/documents/{document_id}/chunks")
    assert chunks.status_code == 200
    assert chunks.json() == [chunk.json()]

    archived = client.patch(f"/api/v1/documents/{document_id}/archive")
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"


def test_knowledge_items_and_relations(client: TestClient) -> None:
    document = create_document(client)
    base_payload = {
        "summary": "Conocimiento estructurado desde el plan.",
        "source_type": "document",
        "source_id": document["id"],
        "municipality_id": document["municipality_id"],
        "department_id": document["department_id"],
        "tags": ["planeación", "metas"],
    }
    first = client.post(
        "/api/v1/knowledge/items",
        json={**base_payload, "title": "Objetivo de transparencia"},
    )
    second = client.post(
        "/api/v1/knowledge/items",
        json={**base_payload, "title": "Meta de datos abiertos"},
    )
    assert first.status_code == 201
    assert second.status_code == 201
    first_item = first.json()
    second_item = second.json()

    assert client.get("/api/v1/knowledge/items").status_code == 200
    updated = client.patch(
        f"/api/v1/knowledge/items/{first_item['id']}",
        json={"summary": "Resumen institucional actualizado."},
    )
    assert updated.status_code == 200
    assert updated.json()["summary"] == "Resumen institucional actualizado."

    relation = client.post(
        "/api/v1/knowledge/relations",
        json={
            "source_item_id": first_item["id"],
            "target_item_id": second_item["id"],
            "relation_type": "supports",
            "description": "La meta apoya el objetivo.",
            "confidence_score": 0.9,
        },
    )
    assert relation.status_code == 201
    listed = client.get(
        "/api/v1/knowledge/relations",
        params={"source_item_id": first_item["id"]},
    )
    assert listed.status_code == 200
    assert listed.json() == [relation.json()]

    archived = client.patch(f"/api/v1/knowledge/items/{first_item['id']}/archive")
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"

