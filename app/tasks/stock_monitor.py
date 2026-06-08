"""
Stock Monitor Tasks
"""

from celery import shared_task
from config.database import get_db
from app.notifications.service import NotificationService


@shared_task
def check_low_stock():
    """Check for low stock and create notifications"""
    db = get_db()
    low_stock_products = list(db['products'].find({
        '$expr': {'$lt': ['$stock', '$min_stock']},
        'is_active': True
    }))

    for product in low_stock_products:
        NotificationService.create_notification(
            title='Low Stock Alert',
            message=f"{product['name']} is running low. Current stock: {product['stock']} {product['base_unit']}",
            type='warning',
            link=f"/products/{product['_id']}"
        )

    return {'checked': len(low_stock_products), 'alerts_created': len(low_stock_products)}
