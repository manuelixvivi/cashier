"""
Forecast Scheduler Tasks
"""

from celery import shared_task
from app.forecasting.moving_average import MovingAverageForecast
from app.notifications.service import NotificationService


@shared_task
def run_stock_forecasts():
    """Run stock forecasts for all products"""
    from config.database import get_db
    db = get_db()
    products = list(db['products'].find({'is_active': True}))

    at_risk = []
    for product in products:
        forecast = MovingAverageForecast.forecast_stock(str(product['_id']))
        days = forecast.get('days_until_out_of_stock')
        if days != 'N/A' and days < 7:
            at_risk.append({
                'product': product['name'],
                'days_remaining': days
            })

    if at_risk:
        NotificationService.create_notification(
            title='Stock Forecast Alert',
            message=f"{len(at_risk)} products may run out of stock within 7 days",
            type='warning',
            link='/forecasting'
        )

    return {'products_checked': len(products), 'at_risk': len(at_risk)}
