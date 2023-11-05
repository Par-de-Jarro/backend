from sqlalchemy import Column, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date

from app.common.models.table_model import TableModel
from app.db.database import Base


class SpotBill(Base, TableModel):
    __tablename__ = "spot_bill"

    id_spot_bill = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    id_spot = Column(
        ForeignKey(
            "spot.id_spot",
            name="spot_bill_id_spot_fk",
        ),
        nullable=False,
        index=True,
    )

    spot = relationship("Spot", foreign_keys=id_spot, lazy="joined")

    value = Column(Numeric, nullable=False)

    reference_date = Column(Date, nullable=False, primary_key=False)

    images = Column(ARRAY(String), nullable=True)

    name = Column(String(500), nullable=False)

    description = Column(String(500), nullable=True)
