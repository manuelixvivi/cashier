"""
Inventory Service
"""

from bson import ObjectId
from app.inventory.model import InventoryMovement, StockOpname, StockTransfer
from app.inventory.repository import InventoryRepository, StockOpnameRepository, StockTransferRepository
from app.products.repository import ProductRepository
from app.core.exceptions import NotFoundException, ValidationException


class InventoryService:
    @classmethod
    def goods_receipt(cls, product_id, quantity, unit, reference_id=None, 
                      reference_type=None, notes='', created_by=None, location='default'):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        base_qty = product.convert_to_base(unit, quantity)
        ProductRepository.update_stock(product_id, base_qty)

        movement = InventoryMovement(
            product_id=ObjectId(product_id),
            movement_type='goods_receipt',
            quantity=base_qty,
            unit=unit,
            reference_id=ObjectId(reference_id) if reference_id else None,
            reference_type=reference_type,
            notes=notes,
            warehouse_location=location,
            created_by=ObjectId(created_by) if created_by else None
        )
        InventoryRepository.create_movement(movement)
        return movement.to_dict()

    @classmethod
    def stock_out(cls, product_id, quantity, unit, reference_id=None,
                  reference_type=None, notes='', created_by=None, location='default'):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        base_qty = product.convert_to_base(unit, quantity)
        if product.stock < base_qty:
            raise ValidationException(f'Insufficient stock. Available: {product.stock} {product.base_unit}')

        ProductRepository.update_stock(product_id, -base_qty)

        movement = InventoryMovement(
            product_id=ObjectId(product_id),
            movement_type='stock_out',
            quantity=-base_qty,
            unit=unit,
            reference_id=ObjectId(reference_id) if reference_id else None,
            reference_type=reference_type,
            notes=notes,
            warehouse_location=location,
            created_by=ObjectId(created_by) if created_by else None
        )
        InventoryRepository.create_movement(movement)
        return movement.to_dict()

    @classmethod
    def stock_adjustment(cls, product_id, new_qty, unit, reason='', created_by=None, location='default'):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        new_base_qty = product.convert_to_base(unit, new_qty)
        difference = new_base_qty - product.stock
        ProductRepository.update_stock(product_id, difference)

        movement = InventoryMovement(
            product_id=ObjectId(product_id),
            movement_type='stock_adjustment',
            quantity=difference,
            unit=unit,
            notes=f'Adjustment: {reason}. New qty: {new_qty} {unit}',
            warehouse_location=location,
            created_by=ObjectId(created_by) if created_by else None
        )
        InventoryRepository.create_movement(movement)
        return movement.to_dict()

    @classmethod
    def stock_opname(cls, product_id, physical_qty, unit, notes='', created_by=None):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        physical_base_qty = product.convert_to_base(unit, physical_qty)
        difference = physical_base_qty - product.stock

        opname = StockOpname(
            product_id=ObjectId(product_id),
            system_qty=product.stock,
            physical_qty=physical_base_qty,
            difference=difference,
            unit=unit,
            notes=notes,
            created_by=ObjectId(created_by) if created_by else None
        )
        StockOpnameRepository.create(opname)
        ProductRepository.update_stock(product_id, difference)

        return opname.to_dict()

    @classmethod
    def stock_transfer(cls, product_id, from_location, to_location, quantity, unit,
                       notes='', created_by=None):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        base_qty = product.convert_to_base(unit, quantity)
        source_stock = InventoryRepository.get_stock_by_location(product_id, from_location)
        if source_stock < base_qty:
            raise ValidationException(f'Insufficient stock at {from_location}')

        transfer = StockTransfer(
            product_id=ObjectId(product_id),
            from_location=from_location,
            to_location=to_location,
            quantity=base_qty,
            unit=unit,
            status='pending',
            notes=notes,
            created_by=ObjectId(created_by) if created_by else None
        )
        StockTransferRepository.create(transfer)
        return transfer.to_dict()

    @classmethod
    def complete_transfer(cls, transfer_id, created_by=None):
        db = __import__('config.database').database.get_db()
        transfer_data = db['stock_transfers'].find_one({'_id': ObjectId(transfer_id)})
        if not transfer_data:
            raise NotFoundException('Transfer not found')

        if transfer_data['status'] != 'pending':
            raise ValidationException('Transfer is not pending')

        out_movement = InventoryMovement(
            product_id=transfer_data['product_id'],
            movement_type='stock_transfer',
            quantity=-transfer_data['quantity'],
            unit=transfer_data['unit'],
            reference_id=transfer_data['_id'],
            reference_type='transfer_out',
            warehouse_location=transfer_data['from_location'],
            created_by=ObjectId(created_by) if created_by else None
        )
        InventoryRepository.create_movement(out_movement)

        in_movement = InventoryMovement(
            product_id=transfer_data['product_id'],
            movement_type='stock_transfer',
            quantity=transfer_data['quantity'],
            unit=transfer_data['unit'],
            reference_id=transfer_data['_id'],
            reference_type='transfer_in',
            warehouse_location=transfer_data['to_location'],
            created_by=ObjectId(created_by) if created_by else None
        )
        InventoryRepository.create_movement(in_movement)

        StockTransferRepository.update_status(transfer_id, 'completed')
        return {'message': 'Transfer completed'}

    @classmethod
    def get_product_movements(cls, product_id, limit=50):
        movements = InventoryRepository.get_movements_by_product(product_id, limit)
        return [m.to_dict() for m in movements]

    @classmethod
    def get_product_opnames(cls, product_id, limit=20):
        opnames = StockOpnameRepository.get_by_product(product_id, limit)
        return [o.to_dict() for o in opnames]
