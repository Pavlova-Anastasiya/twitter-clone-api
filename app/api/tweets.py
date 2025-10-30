from __future__ import annotations
db.session.commit()
return {"result": True}


@blp.route("/<int:tweet_id>/likes", methods=["POST"])
@blp.response(200, ResultSchema)
def like_tweet(tweet_id: int):
user = get_current_user()
if not db.session.get(Tweet, tweet_id):
raise ApiError("Tweet not found")
exists = db.session.query(Like).filter_by(user_id=user.id, tweet_id=tweet_id).first()
if not exists:
db.session.add(Like(user_id=user.id, tweet_id=tweet_id))
db.session.commit()
return {"result": True}


@blp.route("/<int:tweet_id>/likes", methods=["DELETE"])
@blp.response(200, ResultSchema)
def unlike_tweet(tweet_id: int):
user = get_current_user()
like = db.session.query(Like).filter_by(user_id=user.id, tweet_id=tweet_id).first()
if like:
db.session.delete(like)
db.session.commit()
return {"result": True}


@blp.route("", methods=["GET"])
@blp.response(200, TweetsListSchema)
def get_feed():
user = get_current_user()
# users he follows
follow_ids = [f.following_id for f in user.following]
if not follow_ids:
follow_ids = [user.id] # пусть видит своё


# tweets from followed users with popularity (likes count)
likes_count = db.session.query(
Like.tweet_id, func.count(Like.id).label("lc")
).group_by(Like.tweet_id).subquery()


q = (
db.session.query(Tweet, func.coalesce(likes_count.c.lc, 0).label("pop"))
.outerjoin(likes_count, likes_count.c.tweet_id == Tweet.id)
.filter(Tweet.author_id.in_(follow_ids))
.order_by(db.desc("pop"), db.desc(Tweet.created_at))
.limit(100)
)


tweets = []
for tw, _ in q.all():
author = {"id": tw.author.id, "name": tw.author.name}
attachments = [m.path for m in tw.media_items if m.tweet_id == tw.id]
likes = [
{"user_id": lk.user.id, "name": lk.user.name}
for lk in tw.likes
]
tweets.append({
"id": tw.id,
"content": tw.content,
"attachments": attachments,
"author": author,
"likes": likes,
})
return {"result": True, "tweets": tweets}