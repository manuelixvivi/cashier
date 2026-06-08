"""
Auth Routes - API Endpoints
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.core.response import APIResponse
from app.core.exceptions import ValidationException
from app.auth.service import AuthService
from app.auth.schema import LoginSchema, RegisterSchema, RefreshTokenSchema, ChangePasswordSchema

auth_bp = Blueprint('auth', __name__)

login_schema = LoginSchema()
register_schema = RegisterSchema()
refresh_schema = RefreshTokenSchema()
change_password_schema = ChangePasswordSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    result = AuthService.register(data)
    return APIResponse.success(data=result, message='User registered successfully', status_code=201)


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    result = AuthService.login(data['username'], data['password'])
    return APIResponse.success(data=result, message='Login successful')


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    try:
        data = refresh_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    result = AuthService.refresh_access_token(data['refresh_token'])
    return APIResponse.success(data=result, message='Token refreshed')


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    """Logout user"""
    try:
        data = refresh_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    AuthService.logout(data['refresh_token'])
    return APIResponse.success(message='Logged out successfully')


@auth_bp.route('/logout-all', methods=['POST'])
@jwt_required()
def logout_all():
    """Logout from all devices"""
    user_id = get_jwt_identity()
    AuthService.logout_all(user_id)
    return APIResponse.success(message='Logged out from all devices')


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change password"""
    user_id = get_jwt_identity()

    try:
        data = change_password_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    AuthService.change_password(user_id, data['old_password'], data['new_password'])
    return APIResponse.success(message='Password changed successfully')


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Get current user info"""
    user_id = get_jwt_identity()
    user = AuthService.get_current_user(user_id)
    return APIResponse.success(data=user)
