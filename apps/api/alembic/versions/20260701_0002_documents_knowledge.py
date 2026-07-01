"""Create Documents and Knowledge Core tables.

Revision ID: 20260701_0002
Revises: 20260701_0001
Create Date: 2026-07-01
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260701_0002"
down_revision: str | Sequence[str] | None = "20260701_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def uuid_column() -> sa.Column[sa.Uuid]:
    return sa.Column(
        "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
    )


def timestamp_column(name: str) -> sa.Column[sa.DateTime]:
    return sa.Column(
        name, sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )


def upgrade() -> None:
    """Create document and knowledge storage."""
    op.create_table(
        "documents",
        uuid_column(),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("document_type", sa.String(100), nullable=False),
        sa.Column("source", sa.String(200), nullable=False),
        sa.Column("file_path", sa.String(1000), nullable=False),
        sa.Column("file_name", sa.String(300), nullable=False),
        sa.Column("file_extension", sa.String(20), nullable=False),
        sa.Column("mime_type", sa.String(150), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("checksum", sa.String(128), nullable=False),
        sa.Column("version", sa.String(50), nullable=False),
        sa.Column("status", sa.String(30), server_default="active", nullable=False),
        sa.Column("confidentiality_level", sa.String(30), nullable=False),
        sa.Column("municipality_id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=False),
        sa.Column("uploaded_by_id", sa.Uuid(), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["municipality_id"], ["municipalities.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["department_id"], ["departments.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("municipality_id", "department_id", "uploaded_by_id"):
        op.create_index(op.f(f"ix_documents_{column}"), "documents", [column])

    op.create_table(
        "document_chunks",
        uuid_column(),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column(
            "metadata", sa.JSON(), server_default=sa.text("'{}'"), nullable=False
        ),
        timestamp_column("created_at"),
        sa.ForeignKeyConstraint(
            ["document_id"], ["documents.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "document_id", "chunk_index", name="uq_document_chunk_index"
        ),
    )
    op.create_index(
        op.f("ix_document_chunks_document_id"),
        "document_chunks",
        ["document_id"],
    )

    op.create_table(
        "knowledge_items",
        uuid_column(),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("source_id", sa.Uuid(), nullable=False),
        sa.Column("municipality_id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=True),
        sa.Column("tags", sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
        sa.Column("status", sa.String(30), server_default="active", nullable=False),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["municipality_id"], ["municipalities.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["department_id"], ["departments.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("source_id", "municipality_id", "department_id"):
        op.create_index(
            op.f(f"ix_knowledge_items_{column}"), "knowledge_items", [column]
        )

    op.create_table(
        "knowledge_relations",
        uuid_column(),
        sa.Column("source_item_id", sa.Uuid(), nullable=False),
        sa.Column("target_item_id", sa.Uuid(), nullable=False),
        sa.Column("relation_type", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        timestamp_column("created_at"),
        sa.CheckConstraint(
            "confidence_score >= 0 AND confidence_score <= 1",
            name="ck_knowledge_relation_confidence",
        ),
        sa.CheckConstraint(
            "source_item_id <> target_item_id",
            name="ck_knowledge_relation_distinct_items",
        ),
        sa.ForeignKeyConstraint(
            ["source_item_id"], ["knowledge_items.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["target_item_id"], ["knowledge_items.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("source_item_id", "target_item_id"):
        op.create_index(
            op.f(f"ix_knowledge_relations_{column}"),
            "knowledge_relations",
            [column],
        )


def downgrade() -> None:
    """Remove document and knowledge storage."""
    for column in ("target_item_id", "source_item_id"):
        op.drop_index(
            op.f(f"ix_knowledge_relations_{column}"),
            table_name="knowledge_relations",
        )
    op.drop_table("knowledge_relations")
    for column in ("department_id", "municipality_id", "source_id"):
        op.drop_index(
            op.f(f"ix_knowledge_items_{column}"), table_name="knowledge_items"
        )
    op.drop_table("knowledge_items")
    op.drop_index(
        op.f("ix_document_chunks_document_id"), table_name="document_chunks"
    )
    op.drop_table("document_chunks")
    for column in ("uploaded_by_id", "department_id", "municipality_id"):
        op.drop_index(op.f(f"ix_documents_{column}"), table_name="documents")
    op.drop_table("documents")
