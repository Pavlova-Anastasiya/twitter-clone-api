from app import db
from app.models import User


API = {"alice": "alice-key", "bob": "bob-key"}




def seed_users():
a = User(name="Alice", api_key=API["alice"])
b = User(name="Bob", api_key=API["bob"])
db.session.add_all([a, b])
db.session.commit()
return a, b




def test_create_like_unlike_and_feed(client, app):
with app.app_context():
alice, bob = seed_users()


# Alice создаёт твит
r = client.post(
"/api/tweets",
headers={"api-key": API["alice"]},
json={"tweet_data": "Hello test!", "tweet_media_ids": []},
)
assert r.status_code == 200
tid = r.get_json()["tweet_id"]


# Bob лайкает
r = client.post(f"/api/tweets/{tid}/likes", headers={"api-key": API["bob"]})
assert r.status_code == 200


# Лента Alice (должен быть её твит)
r = client.get("/api/tweets", headers={"api-key": API["alice"]})
data = r.get_json()
assert data["result"] is True
assert any(t["id"] == tid for t in data["tweets"]) # твит в ленте


# Bob снимает лайк
r = client.delete(f"/api/tweets/{tid}/likes", headers={"api-key": API["bob"]})
assert r.status_code == 200


# Alice удаляет свой твит
r = client.delete(f"/api/tweets/{tid}", headers={"api-key": API["alice"]})
assert r.status_code == 200