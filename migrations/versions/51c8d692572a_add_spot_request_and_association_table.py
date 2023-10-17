"""add_spot_request_and_association_table

Revision ID: 51c8d692572a
Revises: 917df9194b2a
Create Date: 2023-10-17 08:57:11.828813

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

from app.spot.schemas.spot_entry_request import EntryRequestStatus

# revision identifiers, used by Alembic.
revision = "51c8d692572a"
down_revision = "917df9194b2a"
branch_labels = None
depends_on = None


def upgrade():
    enum = ENUM("ACCEPTED", "NOT_ACCEPTED", "REQUEST", name="entryrequeststatus", create_type=False)
    enum.create(op.get_bind(), checkfirst=False)

    op.create_table(
        "spot_entry_request",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_spot_entry_request",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("status", enum, default=EntryRequestStatus.REQUEST),
        sa.Column("id_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_spot", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_spot"], ["spot.id_spot"], name="spot_spot_entry_request_id_spot"
        ),
        sa.ForeignKeyConstraint(
            ["id_user"], ["user.id_user"], name="user_spot_entry_request_id_user"
        ),
        sa.PrimaryKeyConstraint("id_spot_entry_request"),
        sa.UniqueConstraint("id_spot_entry_request"),
    )
    op.create_index(
        op.f("ix_spot_entry_request_id_spot"), "spot_entry_request", ["id_spot"], unique=False
    )
    op.create_index(
        op.f("ix_spot_entry_request_id_user"), "spot_entry_request", ["id_user"], unique=False
    )
    op.create_table(
        "spot_user",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_spot_user",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_spot", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["id_spot"], ["spot.id_spot"], name="spot_user_spot_id_spot"),
        sa.ForeignKeyConstraint(["id_user"], ["user.id_user"], name="user_spot_id_user"),
        sa.PrimaryKeyConstraint("id_spot_user"),
        sa.UniqueConstraint("id_spot_user"),
    )
    op.create_index(op.f("ix_spot_user_id_spot"), "spot_user", ["id_spot"], unique=False)
    op.create_index(op.f("ix_spot_user_id_user"), "spot_user", ["id_user"], unique=False)
    op.create_unique_constraint(None, "university", ["id_university"])


def downgrade():
    op.drop_index(op.f("ix_spot_user_id_user"), table_name="spot_user")
    op.drop_index(op.f("ix_spot_user_id_spot"), table_name="spot_user")
    op.drop_table("spot_user")
    op.drop_index(op.f("ix_spot_entry_request_id_user"), table_name="spot_entry_request")
    op.drop_index(op.f("ix_spot_entry_request_id_spot"), table_name="spot_entry_request")
    op.drop_table("spot_entry_request")
    ENUM(name="entryrequeststatus").drop(op.get_bind(), checkfirst=False)
