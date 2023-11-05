from sqlalchemy import Column, Enum, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models.table_model import TableModel
from app.db.database import Base
from app.spot.schemas.spot_entry_request import EntryRequestStatus


class SpotEntryRequest(Base, TableModel):
    __tablename__ = "spot_entry_request"

    id_spot_entry_request = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    status = Column(Enum(EntryRequestStatus), default=EntryRequestStatus.REQUEST)

    id_user = Column(
        ForeignKey(
            "user.id_user",
            name="user_spot_entry_request_id_user",
        ),
        nullable=False,
        index=True,
    )

    user = relationship("User", foreign_keys=id_user, lazy="joined")
    id_spot = Column(
        ForeignKey(
            "spot.id_spot",
            name="spot_spot_entry_request_id_spot",
        ),
        nullable=False,
        index=True,
    )

    spot = relationship("Spot", foreign_keys=id_spot, lazy="joined")
