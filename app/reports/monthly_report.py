"""
Monthly Report Generator
"""

from datetime import datetime
from config.database import get_db


class MonthlyReport:
    """Generate monthly reports"""

    @classmethod
    def generate(cls, year=None, month=None):
        """Generate monthly report"""
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month

        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)

        db = get_db()

        # Monthly summary
        summary_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'total_sales': {'$sum': '$total_amount'},
                'total_transactions': {'$sum': 1},
                'avg_transaction': {'$avg': '$total_amount'},
                'total_items': {'$sum': {'$size': '$items'}}
            }}
        ]
        summary_result = list(db['sales'].aggregate(summary_pipeline))
        summary = summary_result[0] if summary_result else {
            'total_sales': 0, 'total_transactions': 0, 
            'avg_transaction': 0, 'total_items': 0
        }

        # Weekly breakdown
        weekly_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$week': '$created_at'},
                'total_sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        weekly_breakdown = list(db['sales'].aggregate(weekly_pipeline))

        # Category breakdown
        category_pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lt': end}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$lookup': {
                'from': 'products',
                'localField': 'items.product_id',
                'foreignField': '_id',
                'as': 'product'
            }},
            {'$unwind': '$product'},
            {'$group': {
                '_id': '$product.category',
                'total_sales': {'$sum': '$items.total'},
                'total_qty': {'$sum': '$items.qty'}
            }},
            {'$sort': {'total_sales': -1}}
        ]
        category_breakdown = list(db['sales'].aggregate(category_pipeline))

        return {
            'year': year,
            'month': month,
            'summary': summary,
            'weekly_breakdown': weekly_breakdown,
            'category_breakdown': category_breakdown
        }
