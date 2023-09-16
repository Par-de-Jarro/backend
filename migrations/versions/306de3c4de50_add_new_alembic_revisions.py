"""add_new_alembic_revisions

Revision ID: 306de3c4de50
Revises: 547bea62c997
Create Date: 2023-09-05 04:16:05.078477

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "306de3c4de50"
down_revision = "547bea62c997"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user", sa.Column("bio", sa.String(length=500), nullable=True))
    op.add_column("user", sa.Column("birthdate", sa.Date(), nullable=False))
    op.add_column("user", sa.Column("course", sa.String(length=50), nullable=True))
    op.alter_column("user", "profile_img", existing_type=sa.TEXT(), nullable=True)


def downgrade():
    op.alter_column("user", "profile_img", existing_type=sa.TEXT(), nullable=False)
    op.drop_column("user", "course")
    op.drop_column("user", "birthdate")
    op.drop_column("user", "bio")
