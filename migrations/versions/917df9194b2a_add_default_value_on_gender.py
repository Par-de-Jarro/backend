"""add_default_value_on_gender

Revision ID: 917df9194b2a
Revises: 2d931354c1e0
Create Date: 2023-09-25 15:46:06.865916

"""
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "917df9194b2a"
down_revision = "2d931354c1e0"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "user",
        "gender",
        existing_type=postgresql.ENUM(
            "FEMALE", "MALE", "NONBINARY", "UNINFORMED", name="usergender"
        ),
        nullable=False,
        server_default="UNINFORMED",
    )


def downgrade():
    op.alter_column(
        "user",
        "gender",
        existing_type=postgresql.ENUM(
            "FEMALE", "MALE", "NONBINARY", "UNINFORMED", name="usergender"
        ),
        nullable=True,
    )
    op.drop_constraint(None, "university", type_="unique")
