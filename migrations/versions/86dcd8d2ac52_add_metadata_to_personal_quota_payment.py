"""add_metadata_to_personal_quota_payment

Revision ID: 86dcd8d2ac52
Revises: a4cc40877a46
Create Date: 2023-11-04 17:41:11.303589

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "86dcd8d2ac52"
down_revision = "a4cc40877a46"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "personal_quota_payment",
        sa.Column(
            "meta",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("personal_quota_payment", "meta")
