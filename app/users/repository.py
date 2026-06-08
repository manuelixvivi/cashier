"""
User Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.users.model import UserProfile


class UserProfileRepository:
    """User profile repository"""
    COLLECTION = 'user_profiles'

    @classmethod
    def find_by_user_id(cls, user_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'user_id': ObjectId(user_id)})
        return UserProfile.from_dict(data) if data else None

    @classmethod
    def upsert(cls, user_id, profile_data):
        db = get_db()
        profile_data['updated_at'] = datetime.utcnow()
        db[cls.COLLECTION].update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': profile_data},
            upsert=True
        )
        return True
