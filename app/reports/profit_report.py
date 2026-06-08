"""
Profit Report Generator
"""

from datetime import datetime
from config.database import get_db


class ProfitReport:
    """Generate profit and margin reports"""

    @classmethod
    def generate(cls, start_date=None, end_date=None):
        """Generate profit report for date range"""
        if start_date is None:
            start_date = datetime.utcnow().replace(day=1)
        if end_date is None:
            end_date = datetime.utcnow()

        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        db = get_db()

        # Calculate profit per sale
        profit_pipeline = [
            {'$match': {'created_at': {'$gte': start_date, '$lte': end_date}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$lookup': {
                'from': 'products',
                'localField': 'items.product_id',
                'foreignField': '_id',
                'as': 'product'
            }},
            {'$unwind': '$product'},
            {'$project': {
                'revenue': '$items.total',
                'cost': {'$multiply': ['$product.cost_price', '$items.qty']},
                'product_name': '$items.product_name'
            }},
            {'$group': {
                '_id': None,
                'total_revenue': {'$sum': '$revenue'},
                'total_cost': {'$sum': '$cost'},
                'total_profit': {'$sum': {'$subtract': ['$revenue', '$cost']}}
            }}
        ]
        profit_result = list(db['sales'].aggregate(profit_pipeline))
        profit = profit_result[0] if profit_result else {
            'total_revenue': 0, 'total_cost': 0, 'total_profit': 0
        }

        # Margin percentage
        margin = 0
        if profit['total_revenue'] > 0:
            margin = (profit['total_profit'] / profit['total_revenue']) * 100

        # Product profit breakdown
        product_pipeline = [
            {'$match': {'created_at': {'$gte': start_date, '$lte': end_date}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$lookup': {
                'from': 'products',
                'localField': 'items.product_id',
                'foreignField': '_id',
                'as': 'product'
            }},
            {'$unwind': '$product'},
            {'$project': {
                'product_name': '$items.product_name',
                'revenue': '$items.total',
                'cost': {'$multiply': ['$product.cost_price', '$items.qty']}
            }},
            {'$group': {
                '_id': '$product_name',
                'total_revenue': {'$sum': '$revenue'},
                'total_cost': {'$sum': '$cost'},
                'profit': {'$sum': {'$subtract': ['$revenue', '$cost']}}
            }},
            {'$sort': {'profit': -1}}
        ]
        product_profit = list(db['sales'].aggregate(product_pipeline))

        return {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'summary': {
                'total_revenue': profit['total_revenue'],
                'total_cost': profit['total_cost'],
                'total_profit': profit['total_profit'],
                'margin_percentage': round(margin, 2)
            },
            'product_breakdown': product_profit
        }
