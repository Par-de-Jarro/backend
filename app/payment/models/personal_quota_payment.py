from sqlalchemy import Column, Enum, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship

from app.common.models.table_model import TableModel
from app.db.database import Base
from app.payment.schemas.personal_quota_payment import PersonalQuotaPaymentStatus


class PersonalQuotaPayment(Base, TableModel):
    __tablename__ = "personal_quota_payment"

    id_personal_quota_payment = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    id_spot_bill = Column(
        ForeignKey(
            "spot_bill.id_spot_bill",
            name="personal_quota_payment_id_spot_bill_fk",
        ),
        nullable=False,
        index=True,
    )

    spot_bill = relationship(
        "SpotBill",
        foreign_keys=id_spot_bill,
    )

    id_user = Column(
        ForeignKey(
            "user.id_user",
            name="personal_quota_payment_id_user_fk",
        ),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        foreign_keys=id_user,
    )

    value = Column(Numeric, nullable=False)

    images = Column(ARRAY(String), nullable=True)

    status = Column(
        Enum(PersonalQuotaPaymentStatus), nullable=False, server_default="WAITING_FOR_PAYMENT"
    )

    meta = Column(JSONB, nullable=False, server_default=text("'{}'"))
