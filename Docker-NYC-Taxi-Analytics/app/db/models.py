from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TripRecord(Base):
    __tablename__ = "trip_records"

    id = Column(Integer, primary_key=True, index=True)
    pickup_datetime = Column(DateTime, nullable=False)
    dropoff_datetime = Column(DateTime, nullable=False)
    passenger_count = Column(Integer)
    trip_distance = Column(Float)
    total_amount = Column(Float)
    tip_amount = Column(Float, default=0.0)
