"""
Prophet Forecasting Model (optional - requires prophet package)
"""

from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class ProphetForecast:
    """Facebook Prophet forecasting (if available)"""

    @classmethod
    def is_available(cls):
        """Check if prophet is installed"""
        try:
            from prophet import Prophet
            return True
        except ImportError:
            return False

    @classmethod
    def forecast_sales(cls, days=90, forecast_days=30):
        """Forecast sales using Prophet"""
        if not cls.is_available():
            return {
                'method': 'prophet',
                'error': 'Prophet not installed. Install with: pip install prophet',
                'fallback': 'Use moving_average instead'
            }

        from prophet import Prophet
        from config.database import get_db
        import pandas as pd

        end = datetime.utcnow()
        start = end - timedelta(days=days)

        db = get_db()

        # Get daily sales
        pipeline = [
            {'$match': {'created_at': {'$gte': start, '$lte': end}, 'status': 'completed'}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
                'y': {'$sum': '$total_amount'}
            }},
            {'$sort': {'_id': 1}}
        ]
        daily_sales = list(db['sales'].aggregate(pipeline))

        if len(daily_sales) < 30:
            return {
                'method': 'prophet',
                'error': 'Need at least 30 days of data',
                'available': len(daily_sales)
            }

        # Prepare data for Prophet
        df = pd.DataFrame(daily_sales)
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])

        # Fill missing dates
        df = df.set_index('ds').asfreq('D').fillna(0).reset_index()

        # Fit model
        model = Prophet(daily_seasonality=True, yearly_seasonality=False)
        model.fit(df)

        # Make future dataframe
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)

        # Get forecast results
        future_forecast = forecast[forecast['ds'] > df['ds'].max()]

        predictions = []
        for _, row in future_forecast.iterrows():
            predictions.append({
                'date': row['ds'].date().isoformat(),
                'predicted_sales': round(row['yhat'], 2),
                'lower_bound': round(row['yhat_lower'], 2),
                'upper_bound': round(row['yhat_upper'], 2)
            })

        return {
            'method': 'prophet',
            'forecast_days': forecast_days,
            'predictions': predictions[:forecast_days],
            'trend': 'increasing' if predictions[-1]['predicted_sales'] > predictions[0]['predicted_sales'] else 'decreasing'
        }

    @classmethod
    def forecast_product_demand(cls, product_id, days=60, forecast_days=14):
        """Forecast demand for specific product"""
        if not cls.is_available():
            return {
                'method': 'prophet',
                'error': 'Prophet not installed'
            }

        from prophet import Prophet
        from config.database import get_db
        import pandas as pd

        end = datetime.utcnow()
        start = end - timedelta(days=days)

        db = get_db()

        pipeline = [
            {'$match': {
                'created_at': {'$gte': start, '$lte': end},
                'status': 'completed'
            }},
            {'$unwind': '$items'},
            {'$match': {'items.product_id': product_id}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
                'y': {'$sum': '$items.qty'}
            }},
            {'$sort': {'_id': 1}}
        ]
        daily_qty = list(db['sales'].aggregate(pipeline))

        if len(daily_qty) < 14:
            return {
                'method': 'prophet',
                'error': 'Need at least 14 days of data for this product',
                'available': len(daily_qty)
            }

        df = pd.DataFrame(daily_qty)
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])
        df = df.set_index('ds').asfreq('D').fillna(0).reset_index()

        model = Prophet(daily_seasonality=True)
        model.fit(df)

        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)

        future_forecast = forecast[forecast['ds'] > df['ds'].max()]

        total_predicted = future_forecast['yhat'].sum()

        # Get current stock
        product = db['products'].find_one({'_id': __import__('bson').ObjectId(product_id)})
        current_stock = product.get('stock', 0) if product else 0

        return {
            'product_id': product_id,
            'product_name': product['name'] if product else 'Unknown',
            'current_stock': current_stock,
            'forecast_days': forecast_days,
            'predicted_demand': round(total_predicted, 2),
            'daily_predictions': [
                {
                    'date': row['ds'].date().isoformat(),
                    'predicted_qty': round(row['yhat'], 2)
                }
                for _, row in future_forecast.iterrows()
            ],
            'stockout_risk': current_stock < total_predicted,
            'recommended_restock': max(0, round(total_predicted - current_stock, 2))
        }
