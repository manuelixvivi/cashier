"""
Moving Average Forecasting
"""

from datetime import datetime, timedelta
from config.database import get_db


class MovingAverageForecast:
    """Simple moving average forecasting"""

    @classmethod
    def forecast_sales(cls, days=30, window=7):
        """Forecast sales using moving average"""
        end = datetime.utcnow()
        start = end - timedelta(days=days + window)

        db = get_db()

        # Get daily sales
        pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lte': end}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
                'total_sales': {'$sum': '$total_amount'},
                'transactions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        daily_sales = list(db['sales'].aggregate(pipeline))

        if len(daily_sales) < window:
            return {
                'method': 'moving_average',
                'error': 'Not enough data for forecasting',
                'min_required': window,
                'available': len(daily_sales)
            }

        # Calculate moving average
        sales_values = [d['total_sales'] for d in daily_sales]

        forecasts = []
        for i in range(window, len(sales_values)):
            avg = sum(sales_values[i-window:i]) / window
            forecasts.append({
                'date': daily_sales[i]['_id'],
                'actual': sales_values[i],
                'forecast': round(avg, 2),
                'error': round(abs(sales_values[i] - avg), 2)
            })

        # Next day forecast
        last_avg = sum(sales_values[-window:]) / window
        next_date = (datetime.strptime(daily_sales[-1]['_id'], '%Y-%m-%d') + timedelta(days=1)).date()

        return {
            'method': 'moving_average',
            'window': window,
            'historical': forecasts,
            'next_forecast': {
                'date': next_date.isoformat(),
                'predicted_sales': round(last_avg, 2)
            },
            'accuracy': cls._calculate_accuracy(forecasts)
        }

    @classmethod
    def forecast_stock(cls, product_id, days=30):
        """Forecast when stock will run out"""
        end = datetime.utcnow()
        start = end - timedelta(days=days)

        db = get_db()

        # Get daily sales for product
        pipeline = [
            {'$match': {
                'created_at': {'$gte': start, '$lte': end},
                'status': 'completed'
            }},
            {'$unwind': '$items'},
            {'$match': {'items.product_id': product_id}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
                'qty_sold': {'$sum': '$items.qty'}
            }},
            {'$sort': {'_id': 1}}
        ]
        daily_sales = list(db['sales'].aggregate(pipeline))

        if not daily_sales:
            return {
                'product_id': product_id,
                'error': 'No sales data available'
            }

        # Calculate average daily sales
        total_sold = sum(d['qty_sold'] for d in daily_sales)
        avg_daily = total_sold / len(daily_sales)

        # Get current stock
        product = db['products'].find_one({'_id': __import__('bson').ObjectId(product_id)})
        current_stock = product.get('stock', 0) if product else 0

        # Calculate days until out of stock
        if avg_daily <= 0:
            days_until_out = float('inf')
        else:
            days_until_out = current_stock / avg_daily

        return {
            'product_id': product_id,
            'product_name': product['name'] if product else 'Unknown',
            'current_stock': current_stock,
            'avg_daily_sales': round(avg_daily, 2),
            'days_until_out_of_stock': round(days_until_out, 1) if days_until_out != float('inf') else 'N/A',
            'estimated_runout_date': (datetime.utcnow() + timedelta(days=days_until_out)).date().isoformat() if days_until_out != float('inf') else None,
            'recommendation': 'Restock soon' if days_until_out < 7 else 'Stock sufficient'
        }

    @classmethod
    def _calculate_accuracy(cls, forecasts):
        """Calculate forecast accuracy (MAPE)"""
        if not forecasts:
            return 0

        total_error = sum(f['error'] for f in forecasts)
        total_actual = sum(f['actual'] for f in forecasts)

        if total_actual == 0:
            return 0

        mape = (total_error / total_actual) * 100
        return round(100 - mape, 2)  # Accuracy percentage
