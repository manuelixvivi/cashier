"""
Daily Report Generator
"""

from datetime import datetime, timedelta
from config.database import get_db


class DailyReport:
    """Generate daily sales and inventory reports"""

    @classmethod
    def generate(cls, date=None):
        """Generate daily report"""
        if date is None:
            date = datetime.utcnow().date()

        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)

        db = get_db()

        # Sales summary
        sales_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'total_sales': {'$sum': '$total_amount'},
                'total_transactions': {'$sum': 1},
                'total_items': {'$sum': {'$size': '$items'}},
                'avg_transaction': {'$avg': '$total_amount'}
            }}
        ]
        sales_result = list(db['sales'].aggregate(sales_pipeline))
        sales_summary = sales_result[0] if sales_result else {
            'total_sales': 0, 'total_transactions': 0, 
            'total_items': 0, 'avg_transaction': 0
        }

        # Payment method breakdown
        payment_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$group': {
                '_id': '$payment_method',
                'count': {'$sum': 1},
                'total': {'$sum': '$total_amount'}
            }}
        ]
        payment_breakdown = list(db['sales'].aggregate(payment_pipeline))

        # Top products
        top_products_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$group': {
                '_id': '$items.product_id',
                'product_name': {'$first': '$items.product_name'},
                'total_qty': {'$sum': '$items.qty'},
                'total_revenue': {'$sum': '$items.total'}
            }},
            {'$sort': {'total_revenue': -1}},
            {'$limit': 10}
        ]
        top_products = list(db['sales'].aggregate(top_products_pipeline))

        # Inventory movements
        movements_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}}},
            {'$group': {
                '_id': '$movement_type',
                'count': {'$sum': 1},
                'total_qty': {'$sum': '$quantity'}
            }}
        ]
        movements = list(db['inventory_movements'].aggregate(movements_pipeline))

        return {
            'date': date.isoformat(),
            'sales_summary': sales_summary,
            'payment_breakdown': payment_breakdown,
            'top_products': top_products,
            'inventory_movements': movements
        }
