"""
Yearly Report Generator
"""

from datetime import datetime
from config.database import get_db


class YearlyReport:
    """Generate yearly reports"""

    @classmethod
    def generate(cls, year=None):
        """Generate yearly report"""
        if year is None:
            year = datetime.utcnow().year

        start = datetime(year, 1, 1)
        end = datetime(year + 1, 1, 1)

        db = get_db()

        # Yearly summary
        summary_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'total_sales': {'$sum': '$total_amount'},
                'total_transactions': {'$sum': 1},
                'avg_transaction': {'$avg': '$total_amount'}
            }}
        ]
        summary_result = list(db['sales'].aggregate(summary_pipeline))
        summary = summary_result[0] if summary_result else {
            'total_sales': 0, 'total_transactions': 0, 'avg_transaction': 0
        }

        # Monthly breakdown
        monthly_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$month': '$created_at'},
                'total_sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        monthly_breakdown = list(db['sales'].aggregate(monthly_pipeline))

        # Top products of the year
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
            {'$limit': 20}
        ]
        top_products = list(db['sales'].aggregate(top_products_pipeline))

        return {
            'year': year,
            'summary': summary,
            'monthly_breakdown': monthly_breakdown,
            'top_products': top_products
        }
