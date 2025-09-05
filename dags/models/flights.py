from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from models.base import ModelBase


class Flights(ModelBase):
    __tablename__ = 'flights'

    flight_number = Column(String(5))
    seat_capacity = Column(Integer)
    scheduled_departure = Column(DateTime)
    actual_departure = Column(DateTime)
    scheduled_arrival = Column(DateTime)
    actual_arrival = Column(DateTime)
    flight_status = Column(String(20))
    reference_date = Column(Date)

    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)
    airline_id = Column(Integer, ForeignKey("airline.id"), nullable=False)
    departure_airport_id = Column(Integer, ForeignKey("airport.id"), nullable=False)
    arrival_airport_id = Column(Integer, ForeignKey("airport.id"), nullable=False)

    aircraft = relationship("Aircraft", back_populates="flights")
    airline = relationship("Airline", back_populates="flights")
    departure_airport = relationship("Airport", back_populates="departure_flights", foreign_keys=[departure_airport_id])
    arrival_airport = relationship("Airport", back_populates="arrival_flights", foreign_keys=[arrival_airport_id])
