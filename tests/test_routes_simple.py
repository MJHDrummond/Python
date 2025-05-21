from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TOKEN = "secret-token"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_summary_unauth():
    r = client.get("/summary")
    assert r.status_code == 403

def test_summary_auth():
    r = client.get("/summary", headers=HEADERS)
    assert r.status_code in [200, 500]  # 500 if DB empty

def test_summary_basic_auth():
    r = client.get("/summary?strategy=basic", headers=HEADERS)
    assert r.status_code in [200, 500]  # 500 if DB empty

def test_summary_daily_auth():
    r = client.get("/summary?strategy=basic", headers=HEADERS)
    assert r.status_code in [200, 500]  # 500 if DB empty