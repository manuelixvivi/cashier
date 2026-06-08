"""
Auth Repository - Data access layer for User and Token operations
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.auth.model import User, RefreshToken


class UserRepository:
    """User data repository"""
    COLLECTION = 'users'

    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(user_id)})
        return User.from_dict(data) if data else None

    @classmethod
    def find_by_username(cls, username):
        """Find user by username"""
        db = get_db()
        data = db[cls.COLLECTION].find_one({'username': username})
        return User.from_dict(data) if data else None

    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        db = get_db()
        data = db[cls.COLLECTION].find_one({'email': email})
        return User.from_dict(data) if data else None

    @classmethod
    def create(cls, user):
        """Create new user"""
        db = get_db()
        user_dict = {
            '_id': user._id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'full_name': user.full_name,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'last_login': user.last_login
        }
        db[cls.COLLECTION].insert_one(user_dict)
        return user

    @classmethod
    def update(cls, user_id, update_data):
        """Update user data"""
        db = get_db()
        update_data['updated_at'] = datetime.utcnow()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    @classmethod
    def update_last_login(cls, user_id):
        """Update last login timestamp"""
        db = get_db()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'last_login': datetime.utcnow()}}
        )

    @classmethod
    def delete(cls, user_id):
        """Delete user"""
        db = get_db()
        result = db[cls.COLLECTION].delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0

    @classmethod
    def list_all(cls, skip=0, limit=20, filters=None):
        """List all users with pagination"""
        db = get_db()
        query = filters or {}
        cursor = db[cls.COLLECTION].find(query).skip(skip).limit(limit)
        total = db[cls.COLLECTION].count_documents(query)
        users = [User.from_dict(data) for data in cursor]
        return users, total


class RefreshTokenRepository:
    """Refresh token repository"""
    COLLECTION = 'refresh_tokens'

    @classmethod
    def create(cls, token):
        """Create refresh token"""
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': token._id,
            'user_id': token.user_id,
            'token': token.token,
            'expires_at': token.expires_at,
            'revoked': token.revoked,
            'created_at': token.created_at
        })
        return token

    @classmethod
    def find_by_token(cls, token_str):
        """Find token by token string"""
        db = get_db()
        data = db[cls.COLLECTION].find_one({'token': token_str})
        if data:
            return RefreshToken(
                _id=data['_id'],
                user_id=data['user_id'],
                token=data['token'],
                expires_at=data['expires_at'],
                revoked=data.get('revoked', False),
                created_at=data.get('created_at')
            )
        return None

    @classmethod
    def revoke_token(cls, token_str):
        """Revoke a token"""
        db = get_db()
        db[cls.COLLECTION].update_one(
            {'token': token_str},
            {'$set': {'revoked': True}}
        )

    @classmethod
    def revoke_all_user_tokens(cls, user_id):
        """Revoke all tokens for a user"""
        db = get_db()
        db[cls.COLLECTION].update_many(
            {'user_id': ObjectId(user_id)},
            {'$set': {'revoked': True}}
        )

    @classmethod
    def cleanup_expired(cls):
        """Remove expired tokens"""
        db = get_db()
        db[cls.COLLECTION].delete_many({
            'expires_at': {'$lt': datetime.utcnow()}
        })
