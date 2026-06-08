"""
User Management Models
"""

from datetime import datetime
from bson import ObjectId


class UserProfile:
    """Extended user profile"""
    COLLECTION = 'user_profiles'

    def __init__(self, user_id, phone='', address='', avatar='', 
                 emergency_contact='', notes='', _id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.phone = phone
        self.address = address
        self.avatar = avatar
        self.emergency_contact = emergency_contact
        self.notes = notes
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'user_id': str(self.user_id),
            'phone': self.phone,
            'address': self.address,
            'avatar': self.avatar,
            'emergency_contact': self.emergency_contact,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
