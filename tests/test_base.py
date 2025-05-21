import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.models import Base
from app.config.test_settings import test_settings

engine = create_engine(test_settings.database_url)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)  # Ensure tables exist

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {}
app.dependency_overrides["get_db"] = override_get_db

client = TestClient(app)
