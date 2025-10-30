from marshmallow import Schema, fields


class MediaUploadResponse(Schema):
result = fields.Boolean()
media_id = fields.Integer()