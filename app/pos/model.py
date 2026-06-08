"""
POS Models
"""

from datetime import datetime
from bson import ObjectId


class Cart:
    """Shopping cart model"""
    COLLECTION = 'carts'

    def __init__(self, cashier_id, items=None, _id=None):
        self._id = _id or ObjectId()
        self.cashier_id = cashier_id
        self.items = items or []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'cashier_id': str(self.cashier_id),
            'items': self.items,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def subtotal(self):
        return sum(item['total'] for item in self.items)

    @property
    def total_items(self):
        return sum(item['qty'] for item in self.items)


class Receipt:
    """Receipt model"""
    def __init__(self, transaction_code, items, subtotal, discount, tax, total,
                 payment_method, change, cashier_name, store_name, timestamp):
        self.transaction_code = transaction_code
        self.items = items
        self.subtotal = subtotal
        self.discount = discount
        self.tax = tax
        self.total = total
        self.payment_method = payment_method
        self.change = change
        self.cashier_name = cashier_name
        self.store_name = store_name
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'transaction_code': self.transaction_code,
            'store_name': self.store_name,
            'cashier': self.cashier_name,
            'timestamp': self.timestamp.isoformat(),
            'items': self.items,
            'subtotal': self.subtotal,
            'discount': self.discount,
            'tax': self.tax,
            'total': self.total,
            'payment_method': self.payment_method,
            'change': self.change
        }
