"""
Customer Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.customers.model import Customer


class CustomerRepository:
    COLLECTION = 'customers'

    @classmethod
    def find_by_id(cls, customer_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(customer_id)})
        return Customer(**data) if data else None

    @classmethod
    def find_by_phone(cls, phone):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'phone': phone})
        return Customer(**data) if data else None

    @classmethod
    def create(cls, customer):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': customer._id,
            'name': customer.name,
            'phone': customer.phone,
            'email': customer.email,
            'address': customer.address,
            'membership_level': customer.membership_level,
            'points': customer.points,
            'total_spent': customer.total_spent,
            'transaction_count': customer.transaction_count,
            'notes': customer.notes,
            'created_at': customer.created_at,
            'updated_at': customer.updated_at
        })
        return customer

    @classmethod
    def update(cls, customer_id, update_data):
        db = get_db()
        update_data['updated_at'] = datetime.utcnow()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(customer_id)},
            {'$set': update_data}
        )

    @classmethod
    def add_points(cls, customer_id, points, amount):
        db = get_db()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(customer_id)},
            {
                '$inc': {'points': points, 'total_spent': amount, 'transaction_count': 1},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )

    @classmethod
    def list_all(cls, skip=0, limit=20, search=None):
        db = get_db()
        query = {}
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'phone': {'$regex': search, '$options': 'i'}}
            ]
        cursor = db[cls.COLLECTION].find(query).skip(skip).limit(limit)
        total = db[cls.COLLECTION].count_documents(query)
        return [Customer(**data) for data in cursor], total
