from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID

from app.common.models.table_model import TableModel
from app.db.database import Base


class Todo(Base, TableModel):
    __tablename__ = "todo"

    id_todo = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    description = Column(String(50), nullable=False)
