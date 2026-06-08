"""
Notification Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.response import APIResponse
from app.notifications.service import NotificationService

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    limit = request.args.get('limit', 20, type=int)
    result = NotificationService.get_user_notifications(user_id, unread_only, limit)
    return APIResponse.success(data=result)


@notifications_bp.route('/<notification_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    NotificationService.mark_as_read(notification_id)
    return APIResponse.success(message='Notification marked as read')


@notifications_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_read():
    user_id = get_jwt_identity()
    NotificationService.mark_all_read(user_id)
    return APIResponse.success(message='All notifications marked as read')
