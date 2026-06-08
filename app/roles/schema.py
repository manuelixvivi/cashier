"""
Role Schemas
"""

from marshmallow import Schema, fields, validate


class RoleSchema(Schema):
    """Role schema"""
    _id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    permissions = fields.List(fields.String())
    description = fields.String(validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
