"""Add gender column to User table

Revision ID: 2d931354c1e0
Revises: 74c0e1cecd97
Create Date: 2023-09-24 19:07:04.736380

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '2d931354c1e0'
down_revision = '74c0e1cecd97'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('gender', sa.String(length=20), nullable=False, server_default='UNINFORMED'))

    op.create_check_constraint(
        'valid_gender_values',
        'user',
        sa.text(
            "gender IN ('MALE', 'FEMALE', 'NON-BINARY', 'UNINFORMED')"
        )
    )


def downgrade():
    op.drop_constraint('valid_gender_values', 'user', type_='check')

    op.drop_column('user', 'gender')
