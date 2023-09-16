"""add_id_university_on_users_table

Revision ID: 74c0e1cecd97
Revises: 5e3757fd4d0b
Create Date: 2023-09-16 12:22:04.143777

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "74c0e1cecd97"
down_revision = "5e3757fd4d0b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user", sa.Column("id_university", postgresql.UUID(as_uuid=True), nullable=False))
    op.create_index(op.f("ix_user_id_university"), "user", ["id_university"], unique=False)
    op.create_foreign_key(
        "user_university_id_university", "user", "university", ["id_university"], ["id_university"]
    )


def downgrade():
    op.drop_constraint("user_university_id_university", "user", type_="foreignkey")
    op.drop_index(op.f("ix_user_id_university"), table_name="user")
    op.drop_column("user", "id_university")
