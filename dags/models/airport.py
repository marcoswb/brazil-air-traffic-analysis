from sqlalchemy import Column, String, Float, Index
from sqlalchemy.orm import relationship

from models.base import ModelBase


class Airport(ModelBase):
    __tablename__ = 'airport'

    icao_code = Column(String(4), unique=True)
    iata_code = Column(String(3))
    name = Column(String(100))
    municipality = Column(String(100))
    state = Column(String(2))
    country = Column(String(50))
    critical_aircraft = Column(String(5))
    latitude = Column(Float)
    longitude = Column(Float)

    departure_flights = relationship(
        "Flights",
        back_populates="departure_airport",
        cascade="all, delete-orphan",
        foreign_keys="Flights.departure_airport_id"
    )
    arrival_flights = relationship(
        "Flights",
        back_populates="arrival_airport",
        cascade="all, delete-orphan",
        foreign_keys="Flights.arrival_airport_id"
    )

    __table_args__ = (Index('idx_lat_long', latitude, longitude),)