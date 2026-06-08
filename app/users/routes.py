"""
User Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.core.response import APIResponse
from app.core.exceptions import ValidationException
from app.users.service import UserService
from app.users.schema import UserUpdateSchema

users_bp = Blueprint('users', __name__)
user_update_schema = UserUpdateSchema()


@users_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role = request.args.get('role')
    is_active = request.args.get('is_active')

    if is_active is not None:
        is_active = is_active.lower() == 'true'

    result = UserService.list_users(page=page, per_page=per_page, role=role, is_active=is_active)
    return APIResponse.paginated(
        data=result['users'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    user = UserService.get_user(user_id)
    return APIResponse.success(data=user)


@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user"""
    try:
        data = user_update_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    result = UserService.update_user(user_id, data)
    return APIResponse.success(data=result, message='User updated')


@users_bp.route('/<user_id>/deactivate', methods=['POST'])
@jwt_required()
def deactivate_user(user_id):
    """Deactivate user"""
    UserService.deactivate_user(user_id)
    return APIResponse.success(message='User deactivated')
