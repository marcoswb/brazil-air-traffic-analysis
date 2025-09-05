from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from models.base import ModelBase


class Aircraft(ModelBase):
    __tablename__ = 'aircraft'

    icao_code = Column(String(4), unique=True)
    iata_code = Column(ARRAY(String(3)))
    model = Column(String(100))
    critical_aircraft = Column(String(5))

    flights = relationship("Flights", back_populates="aircraft", cascade="all, delete-orphan")