"""
Role Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.roles.model import Role


class RoleRepository:
    """Role data repository"""
    COLLECTION = 'roles'

    @classmethod
    def find_by_id(cls, role_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(role_id)})
        return Role.from_dict(data) if data else None

    @classmethod
    def find_by_name(cls, name):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'name': name})
        return Role.from_dict(data) if data else None

    @classmethod
    def create(cls, role):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': role._id,
            'name': role.name,
            'permissions': role.permissions,
            'description': role.description,
            'created_at': role.created_at,
            'updated_at': role.updated_at
        })
        return role

    @classmethod
    def update(cls, role_id, update_data):
        db = get_db()
        update_data['updated_at'] = datetime.utcnow()
        result = db[cls.COLLECTION].update_one(
            {'_id': ObjectId(role_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, role_id):
        db = get_db()
        result = db[cls.COLLECTION].delete_one({'_id': ObjectId(role_id)})
        return result.deleted_count > 0

    @classmethod
    def list_all(cls):
        db = get_db()
        cursor = db[cls.COLLECTION].find()
        return [Role.from_dict(data) for data in cursor]
