"""
Weekly Report Generator
"""

from datetime import datetime, timedelta
from config.database import get_db


class WeeklyReport:
    """Generate weekly reports"""

    @classmethod
    def generate(cls, year=None, week=None):
        """Generate weekly report"""
        if year is None:
            year = datetime.utcnow().year
        if week is None:
            week = datetime.utcnow().isocalendar()[1]

        # Calculate week start (Monday)
        jan1 = datetime(year, 1, 1)
        week_start = jan1 + timedelta(weeks=week-1, days=-jan1.weekday())
        week_end = week_start + timedelta(days=7)

        db = get_db()

        # Daily breakdown within week
        daily_pipeline = [
            {'$match': {'created_at': {'$gte': week_start, '$lt': week_end}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
                'total_sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        daily_breakdown = list(db['sales'].aggregate(daily_pipeline))

        # Weekly summary
        summary_pipeline = [
            {'$match': {'created_at': {'$gte': week_start, '$lt': week_end}, 'status': 'completed'}},
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

        return {
            'year': year,
            'week': week,
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'summary': summary,
            'daily_breakdown': daily_breakdown
        }
