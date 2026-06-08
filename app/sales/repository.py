"""
Sales Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.sales.model import Sale


class SalesRepository:
    COLLECTION = 'sales'

    @classmethod
    def find_by_id(cls, sale_id):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'_id': ObjectId(sale_id)})
        return Sale(**data) if data else None

    @classmethod
    def find_by_code(cls, code):
        db = get_db()
        data = db[cls.COLLECTION].find_one({'transaction_code': code})
        return Sale(**data) if data else None

    @classmethod
    def create(cls, sale):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': sale._id,
            'transaction_code': sale.transaction_code,
            'items': sale.items,
            'subtotal': sale.subtotal,
            'discount_amount': sale.discount_amount,
            'tax_amount': sale.tax_amount,
            'total_amount': sale.total_amount,
            'payment_method': sale.payment_method,
            'customer_id': sale.customer_id,
            'cashier_id': sale.cashier_id,
            'status': sale.status,
            'notes': sale.notes,
            'created_at': sale.created_at
        })
        return sale

    @classmethod
    def cancel_sale(cls, sale_id, reason=''):
        db = get_db()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(sale_id)},
            {'$set': {'status': 'cancelled', 'cancel_reason': reason, 'cancelled_at': datetime.utcnow()}}
        )

    @classmethod
    def list_all(cls, skip=0, limit=20, start_date=None, end_date=None, cashier_id=None):
        db = get_db()
        query = {}
        if start_date and end_date:
            query['created_at'] = {'$gte': start_date, '$lte': end_date}
        if cashier_id:
            query['cashier_id'] = ObjectId(cashier_id)

        cursor = db[cls.COLLECTION].find(query).sort('created_at', -1).skip(skip).limit(limit)
        total = db[cls.COLLECTION].count_documents(query)
        return [Sale(**data) for data in cursor], total

    @classmethod
    def get_daily_summary(cls, date):
        db = get_db()
        start = datetime(date.year, date.month, date.day)
        end = datetime(date.year, date.month, date.day, 23, 59, 59)

        pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lte': end}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'total_sales': {'$sum': '$total_amount'},
                'total_transactions': {'$sum': 1},
                'total_items': {'$sum': {'$size': '$items'}}
            }}
        ]
        result = list(db[cls.COLLECTION].aggregate(pipeline))
        return result[0] if result else {'total_sales': 0, 'total_transactions': 0, 'total_items': 0}
