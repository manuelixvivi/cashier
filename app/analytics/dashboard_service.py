"""
Dashboard Service - Aggregated analytics for dashboard
"""

from datetime import datetime, timedelta
from config.database import get_db


class DashboardService:
    """Dashboard data service"""

    @classmethod
    def get_dashboard_data(cls):
        """Get all dashboard data"""
        today = datetime.utcnow().date()
        start_today = datetime(today.year, today.month, today.day)
        start_week = start_today - timedelta(days=start_today.weekday())
        start_month = datetime(today.year, today.month, 1)

        db = get_db()

        # Today's sales
        today_pipeline = [
            {'$match': {'created_at': {'$gte': start_today}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }}
        ]
        today_result = list(db['sales'].aggregate(today_pipeline))
        today_data = today_result[0] if today_result else {'sales': 0, 'transactions': 0}

        # Weekly sales
        week_pipeline = [
            {'$match': {'created_at': {'$gte': start_week}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }}
        ]
        week_result = list(db['sales'].aggregate(week_pipeline))
        week_data = week_result[0] if week_result else {'sales': 0, 'transactions': 0}

        # Monthly sales
        month_pipeline = [
            {'$match': {'created_at': {'$gte': start_month}, 'status': 'completed'}},
            {'$group': {
                '_id': None,
                'sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }}
        ]
        month_result = list(db['sales'].aggregate(month_pipeline))
        month_data = month_result[0] if month_result else {'sales': 0, 'transactions': 0}

        # Low stock count
        low_stock = db['products'].count_documents({
            '$expr': {'$lt': ['$stock', '$min_stock']},
            'is_active': True
        })

        # Total products
        total_products = db['products'].count_documents({'is_active': True})

        # Total customers
        total_customers = db['customers'].count_documents({})

        # Recent transactions
        recent = list(db['sales'].find(
            {'status': 'completed'}
        ).sort('created_at', -1).limit(5))

        recent_transactions = [{
            'transaction_code': r['transaction_code'],
            'total': r['total_amount'],
            'time': r['created_at'].isoformat()
        } for r in recent]

        return {
            'today': today_data,
            'week': week_data,
            'month': month_data,
            'inventory': {
                'total_products': total_products,
                'low_stock': low_stock
            },
            'customers': {
                'total': total_customers
            },
            'recent_transactions': recent_transactions
        }
