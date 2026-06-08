"""
Sales Analytics
"""

from datetime import datetime, timedelta
from config.database import get_db


class SalesAnalytics:
    """Sales analytics and insights"""

    @classmethod
    def top_products(cls, limit=10, days=30):
        """Get top selling products"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$group': {
                '_id': '$items.product_id',
                'product_name': {'$first': '$items.product_name'},
                'total_qty': {'$sum': '$items.qty'},
                'total_revenue': {'$sum': '$items.total'},
                'transaction_count': {'$sum': 1}
            }},
            {'$sort': {'total_revenue': -1}},
            {'$limit': limit}
        ]
        return list(db['sales'].aggregate(pipeline))

    @classmethod
    def slow_moving_products(cls, days=30, min_transactions=5):
        """Get slow moving products"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        # Get all active products
        all_products = list(db['products'].find({'is_active': True}))

        # Get sales per product
        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$group': {
                '_id': '$items.product_id',
                'total_qty': {'$sum': '$items.qty'},
                'transaction_count': {'$sum': 1}
            }}
        ]
        sales_data = {str(item['_id']): item for item in db['sales'].aggregate(pipeline)}

        slow_products = []
        for product in all_products:
            pid = str(product['_id'])
            if pid not in sales_data or sales_data[pid]['transaction_count'] < min_transactions:
                slow_products.append({
                    'product_id': pid,
                    'name': product['name'],
                    'stock': product.get('stock', 0),
                    'sales_count': sales_data.get(pid, {}).get('transaction_count', 0),
                    'total_sold': sales_data.get(pid, {}).get('total_qty', 0)
                })

        return sorted(slow_products, key=lambda x: x['sales_count'])[:20]

    @classmethod
    def sales_trend(cls, days=30):
        """Get daily sales trend"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
                'total_sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        return list(db['sales'].aggregate(pipeline))

    @classmethod
    def hourly_distribution(cls, days=7):
        """Get hourly sales distribution"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$hour': '$created_at'},
                'total_sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        return list(db['sales'].aggregate(pipeline))
