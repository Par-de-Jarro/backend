from sqlalchemy import Column, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID

from app.common.models.table_model import TableModel
from app.db.database import Base


class University(Base, TableModel):
    __tablename__ = "university"

    id_university = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    name = Column(String(50), nullable=False, unique=True)

    slug = Column(String(10), nullable=True, unique=True)

    lat = Column(Numeric, nullable=False)

    long = Column(Numeric, nullable=False)
