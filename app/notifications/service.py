"""
Notification Service
"""

from app.notifications.model import Notification
from config.database import get_db
from bson import ObjectId


class NotificationService:
    @classmethod
    def create_notification(cls, title, message, type='info', user_id=None, link=None):
        db = get_db()
        notification = Notification(
            title=title,
            message=message,
            type=type,
            user_id=ObjectId(user_id) if user_id else None,
            link=link
        )
        db[Notification.COLLECTION].insert_one({
            '_id': notification._id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.type,
            'user_id': notification.user_id,
            'is_read': notification.is_read,
            'link': notification.link,
            'created_at': notification.created_at
        })
        return notification.to_dict()

    @classmethod
    def get_user_notifications(cls, user_id, unread_only=False, limit=20):
        db = get_db()
        query = {'user_id': ObjectId(user_id)} if user_id else {'user_id': None}
        if unread_only:
            query['is_read'] = False

        cursor = db[Notification.COLLECTION].find(query).sort('created_at', -1).limit(limit)
        return [Notification(**data).to_dict() for data in cursor]

    @classmethod
    def mark_as_read(cls, notification_id):
        db = get_db()
        db[Notification.COLLECTION].update_one(
            {'_id': ObjectId(notification_id)},
            {'$set': {'is_read': True}}
        )
        return True

    @classmethod
    def mark_all_read(cls, user_id):
        db = get_db()
        db[Notification.COLLECTION].update_many(
            {'user_id': ObjectId(user_id), 'is_read': False},
            {'$set': {'is_read': True}}
        )
        return True
