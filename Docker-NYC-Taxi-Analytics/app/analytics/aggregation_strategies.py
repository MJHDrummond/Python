from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import TripRecord

class AggregationStrategy:
    def summarize(self, db: Session):
        raise NotImplementedError

class BasicSummary(AggregationStrategy):
    def summarize(self, db: Session):
        return db.query(
            func.count(TripRecord.id).label("trip_count"),
            func.avg(TripRecord.total_amount).label("avg_total_amount"),
            func.avg(TripRecord.trip_distance).label("avg_distance"),
            func.avg(TripRecord.tip_amount).label("avg_tip_amount")
        ).one()

class DailySummary(AggregationStrategy):
    def summarize(self, db: Session):
        return db.query(
            func.date(TripRecord.pickup_datetime).label("date"),
            func.count(TripRecord.id).label("trip_count"),
            func.avg(TripRecord.total_amount).label("avg_total_amount"),
            func.avg(TripRecord.tip_amount).label("avg_tip_amount")
        ).group_by(func.date(TripRecord.pickup_datetime)).all()

class Aggregator:
    def __init__(self, strategy: AggregationStrategy):
        self.strategy = strategy

    def run(self, db: Session):
        return self.strategy.summarize(db)
