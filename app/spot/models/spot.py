from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship

from app.common.models.table_model import TableModel
from app.db.database import Base
from app.spot.schemas.spot import SpotType


class Spot(Base, TableModel):
    __tablename__ = "spot"

    id_spot = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    id_user = Column(
        ForeignKey(
            "user.id_user",
            name="spot_user_id_user",
        ),
        nullable=False,
        index=True,
    )

    owner = relationship(
        "User",
        foreign_keys=id_user,
    )

    name = Column(String(50), nullable=False)

    description = Column(String(500), nullable=False)

    personal_quota = Column(Integer, nullable=False)

    images = Column(ARRAY(JSONB), nullable=True)

    type = Column(Enum(SpotType), nullable=False)

    value = Column(Numeric, nullable=False)

    lat = Column(Numeric, nullable=False)

    long = Column(Numeric, nullable=False)

    street = Column(String(500), nullable=False)

    number = Column(String(500), nullable=False)

    complement = Column(String(500), nullable=False)

    city = Column(String(500), nullable=False)

    state = Column(String(2), nullable=False)

    observations = Column(String(500), nullable=False)

    key = Column(JSONB, nullable=False, server_default=text("'{}'"))
