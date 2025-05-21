import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import TripRecord
from datetime import datetime
from app.factory.trip_factory import TripFactory
from app.utils.decorators import log_step
from app.schemas.trip_record_schema import TripRecordSchema

class CSVProcessor:
    def __init__(self, db_session: Session, chunk_size=10000):
        self.db_session = db_session
        self.chunk_size = chunk_size

    @log_step
    def process_file(self, filepath: str):
        # Define columns to use and parse dates
        date_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

        successful_inserts = 0
        failed_inserts = 0

        for chunk in pd.read_csv(filepath, chunksize=self.chunk_size, parse_dates=date_cols):
            records = []
            for _, row in chunk.iterrows():
                # Basic cleaning and type casting
                try:
                    record = TripFactory.from_row(row)
                    #record = TripRecordSchema.to_model(row)
                    records.append(record)
                    successful_inserts += 1
                except Exception as e:
                    # Skip malformed rows or log them
                    print(f"Skipping row due to error: {e}")
                    failed_inserts += 1
                    continue

            self.db_session.bulk_save_objects(records)
            self.db_session.commit()

        return f"Successful Count: {successful_inserts}, Failed Count: {failed_inserts}"
