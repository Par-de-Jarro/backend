"""empty message

Revision ID: 7ff9c245e7c0
Revises: ed7fb8652d4a
Create Date: 2023-10-16 10:10:18.378899

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "7ff9c245e7c0"
down_revision = "ed7fb8652d4a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'spot_user',
        sa.Column('id_spot_user', UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False,
                  primary_key=True),
        sa.Column('id_user', sa.Integer(), sa.ForeignKey('user.id_user', name='spot_user_id_user'), nullable=False,
                  index=True),
        sa.Column('id_spot', sa.Integer(), sa.ForeignKey('spot.id_spot', name='spot_user_id_spot'), nullable=False,
                  index=True),
    )


def downgrade():
    op.drop_table('spot_user')
