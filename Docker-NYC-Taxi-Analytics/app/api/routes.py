from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import SessionLocal
from app.ingestion.processor import CSVProcessor
from app.db.models import TripRecord
from app.auth.security import get_current_user
from app.analytics.aggregation_strategies import Aggregator, BasicSummary, DailySummary
from app.schemas.trip_record_schema import TripRecordSchema
from app.utils.decorators import log_step

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
@log_step
async def upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        _: bool = Depends(get_current_user)
):
    # Save uploaded file temporarily
    contents = await file.read()
    temp_path = f"data/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    processor = CSVProcessor(db)
    try:
        output = processor.process_file(temp_path)
        return {"message": f"Processed file: {file.filename} with {output}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
@log_step
def get_summary(
        strategy: str = "basic",
        db: Session = Depends(get_db),
        _: bool = Depends(get_current_user)
):

    if strategy == 'daily':
        aggregator = Aggregator(DailySummary())
    else:
        aggregator = Aggregator(BasicSummary())

    result = aggregator.run(db)

    if strategy == "daily":
        return [dict(
            date=str(r.date),
            trip_count=r.trip_count,
            avg_total_amount=round(r.avg_total_amount or 0,2),
            avg_tip_amount=round(r.avg_tip_amount or 0, 2)
        ) for r in result]
    else:
        return {
            "trip_count": result.trip_count,
            "avg_total_amount": round(result.avg_total_amount or 0, 2),
            "avg_distance": round(result.avg_distance or 0, 2),
            "avg_tip_amount": round(result.avg_tip_amount or 0, 2)
        }

@router.delete("/clear")
@log_step
def clear_data(
        db: Session = Depends(get_db),
        _: bool = Depends(get_current_user)
):
    deleted_count = db.query(TripRecord).delete()
    db.commit()
    return {"message": f"All trip records deleted, count: {deleted_count}"}

@router.post("/record", status_code=201)
@log_step
def create_trip_record(
    record: TripRecordSchema,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user)
):
    try:
        trip = record.to_model()  # Adapter usage: Pydantic -> ORM
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return {"message": "TripRecord added", "id": trip.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))