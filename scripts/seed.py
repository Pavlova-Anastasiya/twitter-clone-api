from app import create_app, db
from app.models import User, Tweet, Follow, Like


app = create_app()
with app.app_context():
db.create_all()
if not User.query.first():
users = [
User(name="Alice", api_key="alice-key"),
User(name="Bob", api_key="bob-key"),
User(name="Carol", api_key="carol-key"),
]
db.session.add_all(users)
db.session.flush()
# подписки
db.session.add_all([
Follow(follower_id=users[0].id, following_id=users[1].id),
Follow(follower_id=users[0].id, following_id=users[2].id),
Follow(follower_id=users[1].id, following_id=users[2].id),
])
# твиты
tweets = [
Tweet(content="Hello from Alice!", author_id=users[0].id),
Tweet(content="Bob here. Nice day!", author_id=users[1].id),
Tweet(content="Carol posting news.", author_id=users[2].id),
]
db.session.add_all(tweets)
db.session.flush()
# лайки
db.session.add_all([
Like(user_id=users[1].id, tweet_id=tweets[0].id),
Like(user_id=users[2].id, tweet_id=tweets[0].id),
Like(user_id=users[0].id, tweet_id=tweets[2].id),
])
db.session.commit()
print("Seeded: users (api-keys: alice-key, bob-key, carol-key)")
else:
print("Users already present; skipping seed.")