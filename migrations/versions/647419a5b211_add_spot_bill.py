"""add_spot_bill

Revision ID: 647419a5b211
Revises: 51c8d692572a
Create Date: 2023-11-03 21:11:46.541993

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "647419a5b211"
down_revision = "51c8d692572a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "spot_bill",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_spot_bill",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_spot", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("value", sa.Numeric(), nullable=False),
        sa.Column("reference_date", sa.Date(), nullable=False),
        sa.Column("images", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["id_spot"], ["spot.id_spot"], name="spot_bill_id_spot_fk"),
        sa.PrimaryKeyConstraint("id_spot_bill"),
        sa.UniqueConstraint("id_spot_bill"),
    )
    op.create_index(op.f("ix_spot_bill_id_spot"), "spot_bill", ["id_spot"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_spot_bill_id_spot"), table_name="spot_bill")
    op.drop_table("spot_bill")
