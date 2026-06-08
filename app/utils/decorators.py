"""
Custom Decorators
"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.core.exceptions import ForbiddenException


def require_role(*roles):
    """Decorator to require specific roles"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            from app.auth.repository import UserRepository
            user = UserRepository.find_by_id(get_jwt_identity())
            if not user or user.role not in roles:
                raise ForbiddenException('Insufficient permissions')
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def audit_log(action, entity_type):
    """Decorator to log actions"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from flask import request
            from app.audit.service import AuditService
            from flask_jwt_extended import get_jwt_identity

            result = fn(*args, **kwargs)

            try:
                user_id = get_jwt_identity()
                AuditService.log(
                    action=action,
                    entity_type=entity_type,
                    entity_id=kwargs.get('id'),
                    user_id=user_id,
                    ip_address=request.remote_addr
                )
            except:
                pass

            return result
        return wrapper
    return decorator
