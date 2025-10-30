from marshmallow import Schema, fields


class UserShortSchema(Schema):
id = fields.Integer()
name = fields.String()


class ProfileSchema(Schema):
result = fields.Boolean()
user = fields.Dict()