"""add_personal_quota_payment

Revision ID: a4cc40877a46
Revises: 647419a5b211
Create Date: 2023-11-04 11:18:47.621543

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "a4cc40877a46"
down_revision = "647419a5b211"
branch_labels = None
depends_on = None


def upgrade():
    enum = ENUM(
        "WAITING_FOR_PAYMENT", "PAYED", name="personalquotapaymentstatus", create_type=False
    )
    enum.create(op.get_bind(), checkfirst=False)

    op.create_table(
        "personal_quota_payment",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_personal_quota_payment",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_spot_bill", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("value", sa.Numeric(), nullable=False),
        sa.Column("images", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "status",
            enum,
            server_default="WAITING_FOR_PAYMENT",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_spot_bill"],
            ["spot_bill.id_spot_bill"],
            name="personal_quota_payment_id_spot_bill_fk",
        ),
        sa.ForeignKeyConstraint(
            ["id_user"], ["user.id_user"], name="personal_quota_payment_id_user_fk"
        ),
        sa.PrimaryKeyConstraint("id_personal_quota_payment"),
        sa.UniqueConstraint("id_personal_quota_payment"),
    )
    op.create_index(
        op.f("ix_personal_quota_payment_id_spot_bill"),
        "personal_quota_payment",
        ["id_spot_bill"],
        unique=False,
    )
    op.create_index(
        op.f("ix_personal_quota_payment_id_user"),
        "personal_quota_payment",
        ["id_user"],
        unique=False,
    )


def downgrade():
    op.drop_index(op.f("ix_personal_quota_payment_id_user"), table_name="personal_quota_payment")
    op.drop_index(
        op.f("ix_personal_quota_payment_id_spot_bill"), table_name="personal_quota_payment"
    )
    op.drop_table("personal_quota_payment")
    ENUM(name="personalquotapaymentstatus").drop(op.get_bind(), checkfirst=False)
