"""create_user_table

Revision ID: 4c9641dc5c0d
Revises: 2d3b02a0485e
Create Date: 2023-09-04 00:26:36.417737

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4c9641dc5c0d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_user",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=100), nullable=False),
        sa.Column("cellphone", sa.String(length=13), nullable=False),
        sa.Column("document_id", sa.String(length=11), nullable=False),
        sa.Column("profile_img", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id_user"),
        sa.UniqueConstraint("document_id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id_user"),
    )


def downgrade():
    op.drop_table("user")
