"""drop_unused_columns_and_make_others_nullable

Revision ID: 7acbdb1d73e0
Revises: d5a07efee274
Create Date: 2023-09-15 01:54:45.501095

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7acbdb1d73e0"
down_revision = "d5a07efee274"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("spot", "description", existing_type=sa.VARCHAR(length=500), nullable=True)
    op.alter_column("spot", "complement", existing_type=sa.VARCHAR(length=500), nullable=True)
    op.drop_column("spot", "observations")


def downgrade():
    op.add_column(
        "spot",
        sa.Column("observations", sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    )
    op.alter_column("spot", "complement", existing_type=sa.VARCHAR(length=500), nullable=False)
    op.alter_column("spot", "description", existing_type=sa.VARCHAR(length=500), nullable=False)
