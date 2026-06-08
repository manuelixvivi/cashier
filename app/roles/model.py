"""
Role Models
"""

from datetime import datetime
from bson import ObjectId


class Role:
    """Role model"""
    COLLECTION = 'roles'

    def __init__(self, name, permissions=None, description='', _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.permissions = permissions or []
        self.description = description
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'permissions': self.permissions,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            _id=data.get('_id'),
            name=data.get('name'),
            permissions=data.get('permissions', []),
            description=data.get('description', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
