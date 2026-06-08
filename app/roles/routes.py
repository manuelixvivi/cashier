"""
Role Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.core.response import APIResponse
from app.roles.service import RoleService
from app.roles.schema import RoleSchema

roles_bp = Blueprint('roles', __name__)
role_schema = RoleSchema()


@roles_bp.route('/', methods=['GET'])
@jwt_required()
def list_roles():
    """List all roles"""
    roles = RoleService.list_roles()
    return APIResponse.success(data=roles)


@roles_bp.route('/', methods=['POST'])
@jwt_required()
def create_role():
    """Create new role"""
    try:
        data = role_schema.load(request.get_json())
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    result = RoleService.create_role(data)
    return APIResponse.success(data=result, message='Role created', status_code=201)


@roles_bp.route('/<role_id>', methods=['GET'])
@jwt_required()
def get_role(role_id):
    """Get role by ID"""
    role = RoleService.get_role(role_id)
    return APIResponse.success(data=role)


@roles_bp.route('/<role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    """Update role"""
    try:
        data = role_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return APIResponse.error(
            message='Validation error',
            error_code='VALIDATION_ERROR',
            errors=err.messages
        )

    result = RoleService.update_role(role_id, data)
    return APIResponse.success(data=result, message='Role updated')


@roles_bp.route('/<role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    """Delete role"""
    RoleService.delete_role(role_id)
    return APIResponse.success(message='Role deleted')
