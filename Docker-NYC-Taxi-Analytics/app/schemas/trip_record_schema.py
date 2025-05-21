from pydantic import BaseModel
from datetime import datetime

class TripRecordSchema(BaseModel):
    pickup_datetime: datetime
    dropoff_datetime: datetime
    passenger_count: int
    trip_distance: float
    total_amount: float
    tip_amount: float = 0.0

    def to_model(self):
        from app.db.models import TripRecord
        return TripRecord(**self.model_dump())
