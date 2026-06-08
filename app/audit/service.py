"""
Audit Service
"""

from app.audit.model import AuditLog
from config.database import get_db
from bson import ObjectId


class AuditService:
    @classmethod
    def log(cls, action, entity_type, entity_id, user_id=None,
            old_value=None, new_value=None, ip_address=None):
        db = get_db()
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=ObjectId(entity_id) if entity_id else None,
            user_id=ObjectId(user_id) if user_id else None,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address
        )
        db[AuditLog.COLLECTION].insert_one({
            '_id': log._id,
            'action': log.action,
            'entity_type': log.entity_type,
            'entity_id': log.entity_id,
            'user_id': log.user_id,
            'old_value': log.old_value,
            'new_value': log.new_value,
            'ip_address': log.ip_address,
            'created_at': log.created_at
        })
        return log.to_dict()

    @classmethod
    def get_logs(cls, entity_type=None, action=None, user_id=None, 
                 start_date=None, end_date=None, limit=100):
        db = get_db()
        query = {}
        if entity_type:
            query['entity_type'] = entity_type
        if action:
            query['action'] = action
        if user_id:
            query['user_id'] = ObjectId(user_id)
        if start_date and end_date:
            query['created_at'] = {'$gte': start_date, '$lte': end_date}

        cursor = db[AuditLog.COLLECTION].find(query).sort('created_at', -1).limit(limit)
        return [AuditLog(**data).to_dict() for data in cursor]

    @classmethod
    def get_entity_history(cls, entity_type, entity_id, limit=50):
        db = get_db()
        cursor = db[AuditLog.COLLECTION].find({
            'entity_type': entity_type,
            'entity_id': ObjectId(entity_id)
        }).sort('created_at', -1).limit(limit)
        return [AuditLog(**data).to_dict() for data in cursor]
