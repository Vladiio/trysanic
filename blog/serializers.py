from marshmallow import Schema, fields


class IdMixin:
    id = fields.Int(dump_only=True)


class AuthorSchema(Schema, IdMixin):
    name = fields.Str(required=True)


class PostSchema(Schema, IdMixin):
    content = fields.Str(required=True)
    author = fields.Nested(AuthorSchema, required=True)


class CommentSchema(Schema, IdMixin):
    content = fields.Str(required=True)
