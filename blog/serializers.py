from marshmallow import Schema, fields


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
