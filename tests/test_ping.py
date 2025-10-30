from app import create_app


def test_ping():
app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
client = app.test_client()
resp = client.get("/ping")
assert resp.status_code == 200
assert resp.get_json()["result"] is True