"""
Audit Log Models
"""

from datetime import datetime
from bson import ObjectId


class AuditLog:
    """Audit log entry"""
    COLLECTION = 'audit_logs'

    def __init__(self, action, entity_type, entity_id, user_id=None,
                 old_value=None, new_value=None, ip_address=None, _id=None):
        self._id = _id or ObjectId()
        self.action = action  # CREATE, READ, UPDATE, DELETE, LOGIN, LOGOUT
        self.entity_type = entity_type  # product, sale, user, etc.
        self.entity_id = entity_id
        self.user_id = user_id
        self.old_value = old_value
        self.new_value = new_value
        self.ip_address = ip_address
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': str(self.entity_id) if self.entity_id else None,
            'user_id': str(self.user_id) if self.user_id else None,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat()
        }
