
from sqlalchemy import Column, Date, ForeignKey, String, Text, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.common.models.table_model import TableModel
from app.db.database import Base
from app.user.schemas.user import UserGender


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

    name = Column(String(50), nullable=False)

    email = Column(String(50), nullable=False, unique=True)

    password_hash = Column(String(100), nullable=False)

    cellphone = Column(String(13), nullable=False)

    document_id = Column(String(11), nullable=False, unique=True)

    profile_img = Column(Text, nullable=True)

    bio = Column(String(500), nullable=True)

    birthdate = Column(Date, nullable=False)

    course = Column(String(50), nullable=True)

    gender = Column(Enum(UserGender), nullable=False, server_default="UNINFORMED")

    id_university = Column(
        ForeignKey(
            "university.id_university",
            name="user_university_id_university",
        ),
        nullable=False,
        index=True,
    )

    university = relationship(
        "University",
        foreign_keys=id_university,
    )
