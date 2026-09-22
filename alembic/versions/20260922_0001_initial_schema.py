"""initial schema

Revision ID: 20260922_0001
Revises:
Create Date: 2026-09-22 00:00:00.000000

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260922_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)

    op.create_table(
        "verification_token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_verification_token_id"), "verification_token", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_verification_token_token"), "verification_token", ["token"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_verification_token_token"), table_name="verification_token")
    op.drop_index(op.f("ix_verification_token_id"), table_name="verification_token")
    op.drop_table("verification_token")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")