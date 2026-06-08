"""
Customer Models
"""

from datetime import datetime
from bson import ObjectId


class Customer:
    """Customer model"""
    COLLECTION = 'customers'

    def __init__(self, name, phone='', email='', address='',
                 membership_level='regular', points=0, notes='', _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.membership_level = membership_level
        self.points = points
        self.notes = notes
        self.total_spent = 0
        self.transaction_count = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'membership_level': self.membership_level,
            'points': self.points,
            'total_spent': self.total_spent,
            'transaction_count': self.transaction_count,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
