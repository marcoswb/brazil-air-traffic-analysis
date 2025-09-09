from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base import ModelBase


class Airline(ModelBase):
    __tablename__ = 'airline'

    icao_code = Column(String(4), unique=True)
    iata_code = Column(String(3))
    name = Column(String(100))
    headquarters_country = Column(String(50))

    flights = relationship("Flights", back_populates="airline", cascade="all, delete-orphan")