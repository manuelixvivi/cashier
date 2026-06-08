"""
Audit Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.audit.service import AuditService

audit_bp = Blueprint('audit', __name__)


@audit_bp.route('/', methods=['GET'])
@jwt_required()
def get_logs():
    entity_type = request.args.get('entity_type')
    action = request.args.get('action')
    user_id = request.args.get('user_id')
    limit = request.args.get('limit', 100, type=int)
    result = AuditService.get_logs(
        entity_type=entity_type,
        action=action,
        user_id=user_id,
        limit=limit
    )
    return APIResponse.success(data=result)


@audit_bp.route('/<entity_type>/<entity_id>', methods=['GET'])
@jwt_required()
def get_entity_history(entity_type, entity_id):
    limit = request.args.get('limit', 50, type=int)
    result = AuditService.get_entity_history(entity_type, entity_id, limit)
    return APIResponse.success(data=result)
