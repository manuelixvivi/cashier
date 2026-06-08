"""
Supplier Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.suppliers.model import Supplier


class SupplierRepository:
    COLLECTION = 'suppliers'

    @classmethod
    def find_by_id(cls, supplier_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(supplier_id)})
        return Supplier(**data) if data else None

    @classmethod
    def create(cls, supplier):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': supplier._id,
            'name': supplier.name,
            'contact_person': supplier.contact_person,
            'phone': supplier.phone,
            'email': supplier.email,
            'address': supplier.address,
            'tax_id': supplier.tax_id,
            'notes': supplier.notes,
            'is_active': supplier.is_active,
            'created_at': supplier.created_at,
            'updated_at': supplier.updated_at
        })
        return supplier

    @classmethod
    def update(cls, supplier_id, update_data):
        db = get_db()
        update_data['updated_at'] = datetime.utcnow()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(supplier_id)},
            {'$set': update_data}
        )

    @classmethod
    def list_all(cls, skip=0, limit=20):
        db = get_db()
        cursor = db[cls.COLLECTION].find().skip(skip).limit(limit)
        total = db[cls.COLLECTION].count_documents({})
        return [Supplier(**data) for data in cursor], total
