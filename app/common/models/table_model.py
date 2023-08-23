from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime


class TableModel:

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=None)
