"""
Auth Models - User and Role data structures
"""

from datetime import datetime
from bson import ObjectId


class User:
    """User model"""
    COLLECTION = 'users'

    def __init__(self, username, email, password_hash, full_name='', 
                 role='cashier', is_active=True, _id=None, created_at=None, 
                 updated_at=None, last_login=None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.last_login = last_login

    def to_dict(self):
        return {
            '_id': str(self._id),
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            _id=data.get('_id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            full_name=data.get('full_name', ''),
            role=data.get('role', 'cashier'),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            last_login=data.get('last_login')
        )


class RefreshToken:
    """Refresh Token model"""
    COLLECTION = 'refresh_tokens'

    def __init__(self, user_id, token, expires_at, _id=None, created_at=None, revoked=False):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
        self.revoked = revoked
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'user_id': str(self.user_id),
            'token': self.token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'revoked': self.revoked,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
