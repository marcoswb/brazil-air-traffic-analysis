from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from controllers.database import Base


class ModelBase(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)