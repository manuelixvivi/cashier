"""
Purchase Models
"""

from datetime import datetime
from bson import ObjectId


class PurchaseOrder:
    """Purchase order model"""
    COLLECTION = 'purchase_orders'

    def __init__(self, supplier_id, items, total_amount, status='draft',
                 notes='', created_by=None, _id=None):
        self._id = _id or ObjectId()
        self.po_code = f"PO-{datetime.utcnow().strftime('%Y%m%d')}-{str(self._id)[-6:]}"
        self.supplier_id = supplier_id
        self.items = items
        self.total_amount = total_amount
        self.status = status
        self.notes = notes
        self.created_by = created_by
        self.created_at = datetime.utcnow()
        self.ordered_at = None
        self.received_at = None

    def to_dict(self):
        return {
            '_id': str(self._id),
            'po_code': self.po_code,
            'supplier_id': str(self.supplier_id),
            'items': self.items,
            'total_amount': self.total_amount,
            'status': self.status,
            'notes': self.notes,
            'created_by': str(self.created_by) if self.created_by else None,
            'created_at': self.created_at.isoformat(),
            'ordered_at': self.ordered_at.isoformat() if self.ordered_at else None,
            'received_at': self.received_at.isoformat() if self.received_at else None
        }
