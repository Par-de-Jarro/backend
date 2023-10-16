from sqlalchemy import Column, Enum, ForeignKey, Integer, text
from sqlalchemy.dialects.postgresql import UUID
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

    status = Column(
        Enum(EntryRequestStatus),
        default=EntryRequestStatus.REQUEST
    )

    id_user = Column(Integer, ForeignKey("user.id_user"))

    id_spot = Column(Integer, ForeignKey("spot.id_spot"))
