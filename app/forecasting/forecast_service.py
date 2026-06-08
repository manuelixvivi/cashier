"""
Forecast Service - Unified forecasting interface
"""

from app.forecasting.moving_average import MovingAverageForecast
from app.forecasting.prophet_model import ProphetForecast


class ForecastService:
    """Unified forecasting service"""

    @classmethod
    def sales_forecast(cls, method='moving_average', days=30, **kwargs):
        """Get sales forecast using specified method"""
        if method == 'prophet' and ProphetForecast.is_available():
            return ProphetForecast.forecast_sales(days=kwargs.get('historical_days', 90), 
                                                   forecast_days=days)
        return MovingAverageForecast.forecast_sales(days=days, 
                                                     window=kwargs.get('window', 7))

    @classmethod
    def stock_forecast(cls, product_id, days=30):
        """Get stock runout forecast"""
        return MovingAverageForecast.forecast_stock(product_id, days=days)

    @classmethod
    def product_demand_forecast(cls, product_id, method='prophet', days=14):
        """Get product demand forecast"""
        if method == 'prophet' and ProphetForecast.is_available():
            return ProphetForecast.forecast_product_demand(product_id, forecast_days=days)

        # Fallback to moving average for product demand
        return MovingAverageForecast.forecast_stock(product_id, days=days)

    @classmethod
    def get_available_methods(cls):
        """Get list of available forecasting methods"""
        methods = ['moving_average']
        if ProphetForecast.is_available():
            methods.append('prophet')
        return methods
