"""add_zip_code_on_spot

Revision ID: d5a07efee274
Revises: 22093649178c
Create Date: 2023-09-14 13:35:15.147502

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d5a07efee274"
down_revision = "22093649178c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("spot", sa.Column("zip_code", sa.String(length=50), nullable=True))


def downgrade():
    op.drop_column("spot", "zip_code")
