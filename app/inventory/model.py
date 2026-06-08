"""
Inventory Models
"""

from datetime import datetime
from bson import ObjectId


class InventoryMovement:
    """Inventory movement record"""
    COLLECTION = 'inventory_movements'

    def __init__(self, product_id, movement_type, quantity, unit,
                 reference_id=None, reference_type=None, notes='',
                 warehouse_location='default', created_by=None, _id=None):
        self._id = _id or ObjectId()
        self.product_id = product_id
        self.movement_type = movement_type
        self.quantity = quantity
        self.unit = unit
        self.reference_id = reference_id
        self.reference_type = reference_type
        self.notes = notes
        self.warehouse_location = warehouse_location
        self.created_by = created_by
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'product_id': str(self.product_id),
            'movement_type': self.movement_type,
            'quantity': self.quantity,
            'unit': self.unit,
            'reference_id': str(self.reference_id) if self.reference_id else None,
            'reference_type': self.reference_type,
            'notes': self.notes,
            'warehouse_location': self.warehouse_location,
            'created_by': str(self.created_by) if self.created_by else None,
            'created_at': self.created_at.isoformat()
        }


class StockOpname:
    """Stock opname record"""
    COLLECTION = 'stock_opnames'

    def __init__(self, product_id, system_qty, physical_qty, unit,
                 difference=None, notes='', created_by=None, _id=None):
        self._id = _id or ObjectId()
        self.product_id = product_id
        self.system_qty = system_qty
        self.physical_qty = physical_qty
        self.difference = difference if difference is not None else physical_qty - system_qty
        self.unit = unit
        self.notes = notes
        self.created_by = created_by
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'product_id': str(self.product_id),
            'system_qty': self.system_qty,
            'physical_qty': self.physical_qty,
            'difference': self.difference,
            'unit': self.unit,
            'notes': self.notes,
            'created_by': str(self.created_by) if self.created_by else None,
            'created_at': self.created_at.isoformat()
        }


class StockTransfer:
    """Stock transfer between locations"""
    COLLECTION = 'stock_transfers'

    def __init__(self, product_id, from_location, to_location, quantity, unit,
                 status='pending', notes='', created_by=None, _id=None):
        self._id = _id or ObjectId()
        self.product_id = product_id
        self.from_location = from_location
        self.to_location = to_location
        self.quantity = quantity
        self.unit = unit
        self.status = status
        self.notes = notes
        self.created_by = created_by
        self.created_at = datetime.utcnow()
        self.completed_at = None

    def to_dict(self):
        return {
            '_id': str(self._id),
            'product_id': str(self.product_id),
            'from_location': self.from_location,
            'to_location': self.to_location,
            'quantity': self.quantity,
            'unit': self.unit,
            'status': self.status,
            'notes': self.notes,
            'created_by': str(self.created_by) if self.created_by else None,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
