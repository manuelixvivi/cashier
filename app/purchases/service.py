"""
Purchase Service
"""

from bson import ObjectId
from app.purchases.model import PurchaseOrder
from app.purchases.repository import PurchaseRepository
from app.products.repository import ProductRepository
from app.inventory.service import InventoryService
from app.core.exceptions import NotFoundException, ValidationException


class PurchaseService:
    @classmethod
    def create_po(cls, data, created_by=None):
        items = data.get('items', [])
        total_amount = 0
        for item in items:
            product = ProductRepository.find_by_id(item['product_id'])
            if not product:
                raise NotFoundException(f"Product {item['product_id']} not found")
            item_total = item['qty'] * item['unit_price']
            item['total'] = item_total
            item['product_name'] = product.name
            total_amount += item_total

        po = PurchaseOrder(
            supplier_id=ObjectId(data['supplier_id']),
            items=items,
            total_amount=total_amount,
            status='draft',
            notes=data.get('notes', ''),
            created_by=ObjectId(created_by) if created_by else None
        )
        PurchaseRepository.create(po)
        return po.to_dict()

    @classmethod
    def get_po(cls, po_id):
        po = PurchaseRepository.find_by_id(po_id)
        if not po:
            raise NotFoundException('Purchase order not found')
        return po.to_dict()

    @classmethod
    def list_pos(cls, page=1, per_page=20, status=None):
        skip = (page - 1) * per_page
        pos, total = PurchaseRepository.list_all(skip=skip, limit=per_page, status=status)
        total_pages = (total + per_page - 1) // per_page
        return {
            'purchase_orders': [p.to_dict() for p in pos],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def receive_po(cls, po_id, created_by=None):
        po = PurchaseRepository.find_by_id(po_id)
        if not po:
            raise NotFoundException('Purchase order not found')
        if po.status != 'ordered':
            raise ValidationException('Purchase order must be ordered before receiving')

        for item in po.items:
            InventoryService.goods_receipt(
                product_id=item['product_id'],
                quantity=item['qty'],
                unit=item['unit'],
                reference_id=po_id,
                reference_type='purchase_order',
                notes=f'Received from PO {po.po_code}',
                created_by=created_by
            )

        PurchaseRepository.update_status(po_id, 'received')
        return {'message': 'Purchase order received and stock updated'}

    @classmethod
    def update_po_status(cls, po_id, status):
        po = PurchaseRepository.find_by_id(po_id)
        if not po:
            raise NotFoundException('Purchase order not found')
        PurchaseRepository.update_status(po_id, status)
        return {'message': f'Purchase order status updated to {status}'}
