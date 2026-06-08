"""
Customer Analytics
"""

from datetime import datetime, timedelta
from config.database import get_db


class CustomerAnalytics:
    """Customer analytics and insights"""

    @classmethod
    def top_customers(cls, limit=10, days=30):
        """Get top customers by spending"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed', 'customer_id': {'$ne': None}}},
            {'$group': {
                '_id': '$customer_id',
                'total_spent': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1},
                'avg_transaction': {'$avg': '$total_amount'}
            }},
            {'$sort': {'total_spent': -1}},
            {'$limit': limit}
        ]
        return list(db['sales'].aggregate(pipeline))

    @classmethod
    def customer_segments(cls):
        """Segment customers by spending"""
        db = get_db()

        pipeline = [
            {'$match': {'status': 'completed', 'customer_id': {'$ne': None}}},
            {'$group': {
                '_id': '$customer_id',
                'total_spent': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }}
        ]
        customers = list(db['sales'].aggregate(pipeline))

        # Simple segmentation
        segments = {'vip': 0, 'regular': 0, 'new': 0}
        for c in customers:
            if c['total_spent'] > 1000000:
                segments['vip'] += 1
            elif c['transactions'] > 5:
                segments['regular'] += 1
            else:
                segments['new'] += 1

        return segments

    @classmethod
    def repeat_rate(cls, days=30):
        """Calculate customer repeat rate"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed', 'customer_id': {'$ne': None}}},
            {'$group': {
                '_id': '$customer_id',
                'transactions': {'$sum': 1}
            }}
        ]
        customers = list(db['sales'].aggregate(pipeline))

        total = len(customers)
        repeat = len([c for c in customers if c['transactions'] > 1])

        rate = (repeat / total * 100) if total > 0 else 0

        return {
            'total_customers': total,
            'repeat_customers': repeat,
            'repeat_rate': round(rate, 2)
        }
