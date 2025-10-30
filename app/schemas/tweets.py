from marshmallow import Schema, fields


class TweetCreateSchema(Schema):
tweet_data = fields.String(required=True)
tweet_media_ids = fields.List(fields.Integer(), required=False)


class TweetCreateResponse(Schema):
result = fields.Boolean()
tweet_id = fields.Integer()


class TweetAuthorSchema(Schema):
id = fields.Integer()
name = fields.String()


class LikeInfoSchema(Schema):
user_id = fields.Integer()
name = fields.String()


class TweetOutSchema(Schema):
id = fields.Integer()
content = fields.String()
attachments = fields.List(fields.String())
author = fields.Nested(TweetAuthorSchema)
likes = fields.List(fields.Nested(LikeInfoSchema))


class TweetsListSchema(Schema):
result = fields.Boolean()
tweets = fields.List(fields.Nested(TweetOutSchema))