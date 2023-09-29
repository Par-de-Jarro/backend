"""Add Spot-User association table

Revision ID: ed7fb8652d4a
Revises: 917df9194b2a
Create Date: 2023-09-28 23:18:32.893811

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID, text

# revision identifiers, used by Alembic.
revision = 'ed7fb8652d4a'
down_revision = '917df9194b2a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'spot_user',
        sa.Column('id_spot_user', UUID(as_uuid=True), server_default=text('gen_random_uuid()'), nullable=False,
                  primary_key=True),
        sa.Column('id_user', sa.Integer(), nullable=False, index=True),
        sa.Column('id_spot', sa.Integer(), nullable=False, index=True),
    )
    op.create_foreign_key("spot_user_id_user", "spot_user", "user", ["id_user"], ["id_user"])
    op.create_foreign_key("spot_user_id_spot", "spot_user", "spot", ["id_spot"], ["id_spot"])


def downgrade():
    op.drop_table('spot_user')
