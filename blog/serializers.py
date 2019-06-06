from marshmallow import Schema, fields


class PostSchema(Schema):
    content = fields.Str()
