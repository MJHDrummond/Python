from app.db.models import TripRecord

class TripFactory:
    @staticmethod
    def from_row(row):
        return TripRecord(
            pickup_datetime=row['tpep_pickup_datetime'],
            dropoff_datetime=row['tpep_dropoff_datetime'],
            passenger_count=int(row['passenger_count']),
            trip_distance=float(row['trip_distance']),
            total_amount=float(row['total_amount']),
            tip_amount=float(row.get('tip_amount', 0))
        )
