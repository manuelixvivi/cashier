"""
Auth Schemas - Marshmallow validation schemas
"""

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    """User schema for validation"""
    _id = fields.String(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(load_only=True, validate=validate.Length(min=6, max=128))
    full_name = fields.String(validate=validate.Length(max=100))
    role = fields.String(validate=validate.OneOf(['super_admin', 'admin', 'manager', 'cashier', 'inventory_staff']))
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)


class LoginSchema(Schema):
    """Login request schema"""
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class RegisterSchema(Schema):
    """Registration schema"""
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
    full_name = fields.String(validate=validate.Length(max=100))
    role = fields.String(load_default='cashier', validate=validate.OneOf(
        ['admin', 'manager', 'cashier', 'inventory_staff']
    ))


class RefreshTokenSchema(Schema):
    """Refresh token schema"""
    refresh_token = fields.String(required=True)


class ChangePasswordSchema(Schema):
    """Change password schema"""
    old_password = fields.String(required=True, load_only=True)
    new_password = fields.String(required=True, validate=validate.Length(min=6, max=128), load_only=True)
