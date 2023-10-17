"""Add Spot-User association table

Revision ID: ed7fb8652d4a
Revises: bded164558cd
Create Date: 2023-09-28 23:18:32.893811

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ed7fb8652d4a"
down_revision = "bded164558cd"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "spot_user",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_spot_user",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("id_user", postgresql.UUID(), nullable=False, index=True),
        sa.Column("id_spot", postgresql.UUID(), nullable=False, index=True),
    )
    op.create_foreign_key("spot_user_id_user", "spot_user", "user", ["id_user"], ["id_user"])
    op.create_foreign_key("spot_user_id_spot", "spot_user", "spot", ["id_spot"], ["id_spot"])


def downgrade():
    op.drop_table("spot_user")
