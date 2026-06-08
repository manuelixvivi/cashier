"""
Purchase Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.purchases.model import PurchaseOrder


class PurchaseRepository:
    COLLECTION = 'purchase_orders'

    @classmethod
    def find_by_id(cls, po_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(po_id)})
        return PurchaseOrder(**data) if data else None

    @classmethod
    def create(cls, po):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': po._id,
            'po_code': po.po_code,
            'supplier_id': po.supplier_id,
            'items': po.items,
            'total_amount': po.total_amount,
            'status': po.status,
            'notes': po.notes,
            'created_by': po.created_by,
            'created_at': po.created_at,
            'ordered_at': po.ordered_at,
            'received_at': po.received_at
        })
        return po

    @classmethod
    def update_status(cls, po_id, status):
        db = get_db()
        update = {'status': status}
        if status == 'ordered':
            update['ordered_at'] = datetime.utcnow()
        elif status == 'received':
            update['received_at'] = datetime.utcnow()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(po_id)},
            {'$set': update}
        )

    @classmethod
    def list_all(cls, skip=0, limit=20, status=None):
        db = get_db()
        query = {}
        if status:
            query['status'] = status
        cursor = db[cls.COLLECTION].find(query).sort('created_at', -1).skip(skip).limit(limit)
        total = db[cls.COLLECTION].count_documents(query)
        return [PurchaseOrder(**data) for data in cursor], total
