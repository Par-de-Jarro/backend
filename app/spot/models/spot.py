from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID

from app.common.models.table_model import TableModel
from app.db.database import Base


class User(Base, TableModel):
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

    id_user = ...

    user = ...

    name = Column(String(50), nullable=False)

    description = Column(String(500), nullable=False)

    personal_quota = ...

    images = ...

    value = ...

    lat = ...

    long = ...

    street = ...

    number = ...

    complement = ...

    city = ...

    state = ...

    observations = ...

    key = ...
