"""Add gender column to User table

Revision ID: 2d931354c1e0
Revises: 74c0e1cecd97
Create Date: 2023-09-24 19:07:04.736380

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "2d931354c1e0"
down_revision = "74c0e1cecd97"
branch_labels = None
depends_on = None


def upgrade():
    enum = ENUM("FEMALE", "MALE", "NONBINARY", "UNINFORMED", name="usergender", create_type=False)
    enum.create(op.get_bind(), checkfirst=False)

    op.add_column(
        "user",
        sa.Column("gender", enum, nullable=True),
    )


def downgrade():
    op.drop_column("user", "gender")
    ENUM(name="usergender").drop(op.get_bind(), checkfirst=False)
