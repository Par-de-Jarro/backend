"""add_university_table

Revision ID: 5e3757fd4d0b
Revises: 7acbdb1d73e0
Create Date: 2023-09-16 12:15:37.815936

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5e3757fd4d0b"
down_revision = "7acbdb1d73e0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "university",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_university",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("slug", sa.String(length=10), nullable=True),
        sa.Column("lat", sa.Numeric(), nullable=False),
        sa.Column("long", sa.Numeric(), nullable=False),
        sa.PrimaryKeyConstraint("id_university"),
        sa.UniqueConstraint("id_university"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )


def downgrade():
    op.drop_table("university")
