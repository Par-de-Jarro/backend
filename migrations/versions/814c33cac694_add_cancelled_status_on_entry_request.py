"""add_cancelled_status_on_entry_request

Revision ID: 814c33cac694
Revises: 86dcd8d2ac52
Create Date: 2024-02-27 19:50:43.290530

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "814c33cac694"
down_revision = "86dcd8d2ac52"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE entryrequeststatus ADD VALUE 'CANCELLED'")


def downgrade():
    ...
