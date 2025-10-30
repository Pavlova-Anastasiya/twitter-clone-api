from marshmallow import Schema, fields


class ResultSchema(Schema):
result = fields.Boolean(required=True)


class ErrorSchema(Schema):
result = fields.Boolean(dump_default=False)
error_type = fields.String()
error_message = fields.String()