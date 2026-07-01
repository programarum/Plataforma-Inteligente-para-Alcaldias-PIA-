"""Create users, roles and permissions RBAC tables.

Revision ID: 20260701_0003
Revises: 20260701_0002
Create Date: 2026-07-01
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260701_0003"
down_revision: str | Sequence[str] | None = "20260701_0002"
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
    """Create identity and RBAC storage."""
    op.create_table(
        "roles",
        uuid_column(),
        sa.Column("municipality_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_system", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["municipality_id"], ["municipalities.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "municipality_id", "name", name="uq_role_municipality_name"
        ),
    )
    op.create_index(op.f("ix_roles_municipality_id"), "roles", ["municipality_id"])

    op.create_table(
        "permissions",
        uuid_column(),
        sa.Column("code", sa.String(150), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("module", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_table(
        "users",
        uuid_column(),
        sa.Column("municipality_id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=True),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("password_hash", sa.String(500), nullable=False),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("position", sa.String(150), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "is_superuser", sa.Boolean(), server_default=sa.false(), nullable=False
        ),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["municipality_id"], ["municipalities.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["department_id"], ["departments.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    for column in ("municipality_id", "department_id"):
        op.create_index(op.f(f"ix_users_{column}"), "users", [column])

    op.create_table(
        "user_roles",
        uuid_column(),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        timestamp_column("created_at"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
    for column in ("user_id", "role_id"):
        op.create_index(op.f(f"ix_user_roles_{column}"), "user_roles", [column])

    op.create_table(
        "role_permissions",
        uuid_column(),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("permission_id", sa.Uuid(), nullable=False),
        timestamp_column("created_at"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["permission_id"], ["permissions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "role_id", "permission_id", name="uq_role_permission"
        ),
    )
    for column in ("role_id", "permission_id"):
        op.create_index(
            op.f(f"ix_role_permissions_{column}"), "role_permissions", [column]
        )


def downgrade() -> None:
    """Remove identity and RBAC storage."""
    for table, columns in (
        ("role_permissions", ("permission_id", "role_id")),
        ("user_roles", ("role_id", "user_id")),
    ):
        for column in columns:
            op.drop_index(op.f(f"ix_{table}_{column}"), table_name=table)
        op.drop_table(table)
    for column in ("department_id", "municipality_id"):
        op.drop_index(op.f(f"ix_users_{column}"), table_name="users")
    op.drop_table("users")
    op.drop_table("permissions")
    op.drop_index(op.f("ix_roles_municipality_id"), table_name="roles")
    op.drop_table("roles")
