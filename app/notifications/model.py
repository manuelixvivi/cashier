"""
Notification Models
"""

from datetime import datetime
from bson import ObjectId


class Notification:
    """Notification model"""
    COLLECTION = 'notifications'

    def __init__(self, title, message, type='info', user_id=None, 
                 is_read=False, link=None, _id=None):
        self._id = _id or ObjectId()
        self.title = title
        self.message = message
        self.type = type  # info, warning, error, success
        self.user_id = user_id
        self.is_read = is_read
        self.link = link
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'user_id': str(self.user_id) if self.user_id else None,
            'is_read': self.is_read,
            'link': self.link,
            'created_at': self.created_at.isoformat()
        }
