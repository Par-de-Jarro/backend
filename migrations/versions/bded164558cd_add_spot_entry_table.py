"""add spot entry table

Revision ID: bded164558cd
Revises: 917df9194b2a
Create Date: 2023-10-16 10:15:04.000093

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

from app.spot.schemas.spot_entry_request import EntryRequestStatus

# revision identifiers, used by Alembic.
revision = "bded164558cd"
down_revision = "917df9194b2a"
branch_labels = None
depends_on = None


def upgrade():
    enum = ENUM("ACCEPTED", "NOT_ACCEPTED", "REQUEST", name="entryrequeststatus", create_type=False)
    enum.create(op.get_bind(), checkfirst=False)

    op.create_table(
        "spot_entry_request",
        sa.Column(
            "id_spot_entry_request",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("status", enum, default=EntryRequestStatus.REQUEST),
        sa.Column("id_user", postgresql.UUID(), sa.ForeignKey("user.id_user"), nullable=False),
        sa.Column("id_spot", postgresql.UUID(), sa.ForeignKey("spot.id_spot"), nullable=False),
    )


def downgrade():
    op.drop_table("spot_entry_request")
    ENUM(name="entryrequeststatus").drop(op.get_bind(), checkfirst=False)
