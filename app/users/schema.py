"""
User Schemas
"""

from marshmallow import Schema, fields, validate


class UserProfileSchema(Schema):
    """User profile schema"""
    phone = fields.String(validate=validate.Length(max=20))
    address = fields.String(validate=validate.Length(max=255))
    avatar = fields.String()
    emergency_contact = fields.String(validate=validate.Length(max=100))
    notes = fields.String()


class UserUpdateSchema(Schema):
    """User update schema"""
    email = fields.Email()
    full_name = fields.String(validate=validate.Length(max=100))
    role = fields.String(validate=validate.OneOf(['admin', 'manager', 'cashier', 'inventory_staff']))
    is_active = fields.Boolean()
    profile = fields.Nested(UserProfileSchema)
