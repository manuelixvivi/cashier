"""
Sales Models
"""

from datetime import datetime
from bson import ObjectId


class Sale:
    """Sale/Transaction model"""
    COLLECTION = 'sales'

    def __init__(self, items, total_amount, payment_method='cash',
                 discount_amount=0, tax_amount=0, customer_id=None,
                 cashier_id=None, notes='', _id=None):
        self._id = _id or ObjectId()
        self.transaction_code = f"TRX-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{str(self._id)[-4:]}"
        self.items = items
        self.subtotal = sum(item['total'] for item in items)
        self.discount_amount = discount_amount
        self.tax_amount = tax_amount
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.customer_id = customer_id
        self.cashier_id = cashier_id
        self.status = 'completed'
        self.notes = notes
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'transaction_code': self.transaction_code,
            'items': self.items,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'customer_id': str(self.customer_id) if self.customer_id else None,
            'cashier_id': str(self.cashier_id) if self.cashier_id else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
