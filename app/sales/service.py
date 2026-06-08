"""
Sales Service
"""

from datetime import datetime, timedelta
from bson import ObjectId
from app.sales.model import Sale
from app.sales.repository import SalesRepository
from app.products.repository import ProductRepository
from app.inventory.service import InventoryService
from app.customers.repository import CustomerRepository
from app.core.exceptions import NotFoundException, ValidationException


class SalesService:
    @classmethod
    def create_sale(cls, data, cashier_id=None):
        items = data.get('items', [])
        if not items:
            raise ValidationException('No items in sale')

        processed_items = []
        total_amount = 0

        for item in items:
            product = ProductRepository.find_by_id(item['product_id'])
            if not product:
                raise NotFoundException(f"Product {item['product_id']} not found")

            qty = item['qty']
            unit = item.get('unit', product.base_unit)
            unit_price = product.get_price(unit, qty)
            item_total = qty * unit_price

            processed_items.append({
                'product_id': str(product._id),
                'product_name': product.name,
                'qty': qty,
                'unit': unit,
                'unit_price': unit_price,
                'total': item_total
            })

            total_amount += item_total

            InventoryService.stock_out(
                product_id=str(product._id),
                quantity=qty,
                unit=unit,
                reference_type='sale',
                created_by=cashier_id
            )

        discount_amount = data.get('discount_amount', 0)
        total_amount -= discount_amount
        tax_amount = data.get('tax_amount', 0)
        total_amount += tax_amount

        sale = Sale(
            items=processed_items,
            total_amount=total_amount,
            payment_method=data.get('payment_method', 'cash'),
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            customer_id=ObjectId(data['customer_id']) if data.get('customer_id') else None,
            cashier_id=ObjectId(cashier_id) if cashier_id else None,
            notes=data.get('notes', '')
        )

        SalesRepository.create(sale)

        if sale.customer_id:
            CustomerRepository.add_points(sale.customer_id, 0, sale.total_amount)

        return sale.to_dict()

    @classmethod
    def get_sale(cls, sale_id):
        sale = SalesRepository.find_by_id(sale_id)
        if not sale:
            raise NotFoundException('Sale not found')
        return sale.to_dict()

    @classmethod
    def get_sale_by_code(cls, code):
        sale = SalesRepository.find_by_code(code)
        if not sale:
            raise NotFoundException('Sale not found')
        return sale.to_dict()

    @classmethod
    def list_sales(cls, page=1, per_page=20, start_date=None, end_date=None, cashier_id=None):
        skip = (page - 1) * per_page

        if start_date and isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if end_date and isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        sales, total = SalesRepository.list_all(
            skip=skip, limit=per_page,
            start_date=start_date, end_date=end_date,
            cashier_id=cashier_id
        )
        total_pages = (total + per_page - 1) // per_page

        return {
            'sales': [s.to_dict() for s in sales],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def cancel_sale(cls, sale_id, reason=''):
        sale = SalesRepository.find_by_id(sale_id)
        if not sale:
            raise NotFoundException('Sale not found')
        if sale.status == 'cancelled':
            raise ValidationException('Sale already cancelled')

        for item in sale.items:
            InventoryService.goods_receipt(
                product_id=item['product_id'],
                quantity=item['qty'],
                unit=item['unit'],
                reference_id=sale_id,
                reference_type='sale_cancel',
                notes=f'Cancelled sale: {reason}'
            )

        SalesRepository.cancel_sale(sale_id, reason)
        return {'message': 'Sale cancelled and stock restored'}

    @classmethod
    def get_daily_summary(cls, date=None):
        if date is None:
            date = datetime.utcnow()
        return SalesRepository.get_daily_summary(date)
