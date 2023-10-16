"""add spot entry table

Revision ID: bded164558cd
Revises: 7ff9c245e7c0
Create Date: 2023-10-16 10:15:04.000093

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID, ENUM
from app.spot.schemas.spot_entry_request import EntryRequestStatus

# revision identifiers, used by Alembic.
revision = 'bded164558cd'
down_revision = '7ff9c245e7c0'
branch_labels = None
depends_on = None


def upgrade():
    enum = ENUM("ACCEPTED", "NOT_ACCEPTED", "REQUEST", name="entryrequeststatus")
    enum.create(op.get_bind(), checkfirst=False)

    op.create_table(
        "spot_entry_request",
        sa.Column("id_spot_entry_request", UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'),
                  nullable=False, primary_key=True),
        sa.Column("status", enum, default=EntryRequestStatus.REQUEST),
        sa.Column("id_user", sa.Integer(), sa.ForeignKey("user.id_user"), nullable=False),
        sa.Column("id_spot", sa.Integer(), sa.ForeignKey("spot.id_spot"), nullable=False),
    )


def downgrade():
    op.drop_table("spot_entry_request")
    ENUM(name="entryrequeststatus").drop(op.get_bind(), checkfirst=False)
