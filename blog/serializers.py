from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    author = fields.Nested(AuthorSchema, required=True)
