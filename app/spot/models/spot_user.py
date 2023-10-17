from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID

from app.common.models.table_model import TableModel
from app.db.database import Base


class SpotUser(Base, TableModel):
    __tablename__ = "spot_user"

    id_spot_user = Column(
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
            name="user_spot_id_user",
        ),
        nullable=False,
        index=True,
    )

    id_spot = Column(
        ForeignKey(
            "spot.id_spot",
            name="spot_user_spot_id_spot",
        ),
        nullable=False,
        index=True,
    )
