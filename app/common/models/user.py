from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.common.models.table_model import TableModel
from app.db.database import Base


class User(Base, TableModel):
    __tablename__ = "user"
    id_user = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    name = Column(String(50), nulllable=False)
    email = Column(String(50), nulllable=False, unique=True)
    password_hash = Column(String(100), nulllable=False)
    cellphone = Column(String(13), nulllable=False)
    document_id = Column(String(11), nulllable=False, unique=True)
    profile_img = Column(Text, nulllable=False)
    # key=
