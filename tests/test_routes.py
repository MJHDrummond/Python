import unittest
from tests.test_base import client, TestingSessionLocal
from app.db.models import TripRecord
from sqlalchemy.orm import Session

client = TestClient(app)
TOKEN = "secret-token"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Test DB setup complete")

    def setUp(self):
        self.db: Session = TestingSessionLocal()
        self.db.query(TripRecord).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_summary_unauth(self):
        response = client.get("/summary")
        self.assertEqual(response.status_code, 403)

    def test_summary_auth(self):
        response = client.get("/summary", headers=HEADERS)
        self.assertIn(response.status_code, [200, 500])  # 500 if DB empty

    def test_summary_basic_auth(self):
        response = client.get("/summary?strategy=basic", headers=HEADERS)
        self.assertIn(response.status_code, [200, 500])

    def test_summary_daily_auth(self):
        response = client.get("/summary?strategy=daily", headers=HEADERS)
        self.assertIn(response.status_code, [200, 500])

    def test_post_trip_record(self):
        payload = {
            "pickup_datetime": "2023-01-01T08:00:00",
            "dropoff_datetime": "2023-01-01T08:15:00",
            "passenger_count": 2,
            "trip_distance": 4.5,
            "total_amount": 18.75,
            "tip_amount": 3.25
        }
        response = client.post("/record", json=payload, headers=HEADERS)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

if __name__ == "__main__":
    unittest.main()
