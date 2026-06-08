"""
Inventory Analytics
"""

from datetime import datetime, timedelta
from config.database import get_db


class InventoryAnalytics:
    """Inventory analytics and insights"""

    @classmethod
    def stock_turnover(cls, days=30):
        """Calculate stock turnover rate"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        # Get sales quantity per product
        pipeline = [
            {'$match': {'created_at': {'$gte': start}, 'status': 'completed'}},
            {'$unwind': '$items'},
            {'$group': {
                '_id': '$items.product_id',
                'total_sold': {'$sum': '$items.qty'}
            }}
        ]
        sales_data = {str(item['_id']): item['total_sold'] for item in db['sales'].aggregate(pipeline)}

        # Calculate turnover
        products = list(db['products'].find({'is_active': True}))
        turnover = []
        for product in products:
            pid = str(product['_id'])
            sold = sales_data.get(pid, 0)
            stock = product.get('stock', 0)
            avg_stock = stock + (sold / 2)  # Simplified average stock
            rate = sold / avg_stock if avg_stock > 0 else 0

            turnover.append({
                'product_id': pid,
                'name': product['name'],
                'stock': stock,
                'total_sold': sold,
                'turnover_rate': round(rate, 2)
            })

        return sorted(turnover, key=lambda x: x['turnover_rate'], reverse=True)

    @classmethod
    def low_stock_alert(cls):
        """Get products with low stock"""
        db = get_db()
        pipeline = [
            {'$match': {
                '$expr': {'$lt': ['$stock', '$min_stock']},
                'is_active': True
            }},
            {'$project': {
                'name': 1,
                'stock': 1,
                'min_stock': 1,
                'base_unit': 1,
                'shortage': {'$subtract': ['$min_stock', '$stock']}
            }}
        ]
        return list(db['products'].aggregate(pipeline))

    @classmethod
    def stock_value(cls):
        """Calculate total inventory value"""
        db = get_db()
        pipeline = [
            {'$match': {'is_active': True}},
            {'$group': {
                '_id': None,
                'total_value': {'$sum': {'$multiply': ['$stock', '$cost_price']}},
                'total_items': {'$sum': '$stock'}
            }}
        ]
        result = list(db['products'].aggregate(pipeline))
        return result[0] if result else {'total_value': 0, 'total_items': 0}

    @classmethod
    def movement_summary(cls, days=30):
        """Get inventory movement summary"""
        start = datetime.utcnow() - timedelta(days=days)
        db = get_db()

        pipeline = [
            {'$match': {'created_at': {'$gte': start}}},
            {'$group': {
                '_id': '$movement_type',
                'count': {'$sum': 1},
                'total_quantity': {'$sum': '$quantity'}
            }}
        ]
        return list(db['inventory_movements'].aggregate(pipeline))
