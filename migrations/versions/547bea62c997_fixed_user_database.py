"""fixed_user_database

Revision ID: 547bea62c997
Revises: 4c9641dc5c0d
Create Date: 2023-09-04 23:04:19.343093

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "547bea62c997"
down_revision = "4c9641dc5c0d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "user", ["id_user"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    # ### end Alembic commands ###
