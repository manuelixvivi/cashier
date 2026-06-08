"""
Inventory Repository
"""

from datetime import datetime
from bson import ObjectId
from config.database import get_db
from app.inventory.model import InventoryMovement, StockOpname, StockTransfer


class InventoryRepository:
    COLLECTION = 'inventory_movements'

    @classmethod
    def create_movement(cls, movement):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': movement._id,
            'product_id': movement.product_id,
            'movement_type': movement.movement_type,
            'quantity': movement.quantity,
            'unit': movement.unit,
            'reference_id': movement.reference_id,
            'reference_type': movement.reference_type,
            'notes': movement.notes,
            'warehouse_location': movement.warehouse_location,
            'created_by': movement.created_by,
            'created_at': movement.created_at
        })
        return movement

    @classmethod
    def get_movements_by_product(cls, product_id, limit=50):
        db = get_db()
        cursor = db[cls.COLLECTION].find(
            {'product_id': ObjectId(product_id)}
        ).sort('created_at', -1).limit(limit)
        return [InventoryMovement(**data) for data in cursor]

    @classmethod
    def get_stock_by_location(cls, product_id, location='default'):
        db = get_db()
        pipeline = [
            {'$match': {'product_id': ObjectId(product_id), 'warehouse_location': location}},
            {'$group': {'_id': None, 'total': {'$sum': '$quantity'}}}
        ]
        result = list(db[cls.COLLECTION].aggregate(pipeline))
        return result[0]['total'] if result else 0


class StockOpnameRepository:
    COLLECTION = 'stock_opnames'

    @classmethod
    def create(cls, opname):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': opname._id,
            'product_id': opname.product_id,
            'system_qty': opname.system_qty,
            'physical_qty': opname.physical_qty,
            'difference': opname.difference,
            'unit': opname.unit,
            'notes': opname.notes,
            'created_by': opname.created_by,
            'created_at': opname.created_at
        })
        return opname

    @classmethod
    def get_by_product(cls, product_id, limit=20):
        db = get_db()
        cursor = db[cls.COLLECTION].find(
            {'product_id': ObjectId(product_id)}
        ).sort('created_at', -1).limit(limit)
        return [StockOpname(**data) for data in cursor]


class StockTransferRepository:
    COLLECTION = 'stock_transfers'

    @classmethod
    def create(cls, transfer):
        db = get_db()
        db[cls.COLLECTION].insert_one({
            '_id': transfer._id,
            'product_id': transfer.product_id,
            'from_location': transfer.from_location,
            'to_location': transfer.to_location,
            'quantity': transfer.quantity,
            'unit': transfer.unit,
            'status': transfer.status,
            'notes': transfer.notes,
            'created_by': transfer.created_by,
            'created_at': transfer.created_at,
            'completed_at': transfer.completed_at
        })
        return transfer

    @classmethod
    def update_status(cls, transfer_id, status):
        db = get_db()
        update_data = {'status': status}
        if status == 'completed':
            update_data['completed_at'] = datetime.utcnow()
        db[cls.COLLECTION].update_one(
            {'_id': ObjectId(transfer_id)},
            {'$set': update_data}
        )

    @classmethod
    def get_pending_transfers(cls):
        db = get_db()
        cursor = db[cls.COLLECTION].find({'status': 'pending'})
        return [StockTransfer(**data) for data in cursor]
