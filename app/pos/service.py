"""
POS Service - Point of Sale operations
"""

from datetime import datetime
from bson import ObjectId
from app.pos.model import Cart
from app.products.repository import ProductRepository
from app.sales.service import SalesService
from app.auth.repository import UserRepository
from app.core.exceptions import NotFoundException, ValidationException


class POSService:
    """POS service for cart and checkout operations"""

    _carts = {}  # In-memory cart storage (use Redis in production)

    @classmethod
    def get_cart(cls, cashier_id):
        """Get or create cart for cashier"""
        if cashier_id not in cls._carts:
            cls._carts[cashier_id] = Cart(cashier_id=ObjectId(cashier_id))
        return cls._carts[cashier_id]

    @classmethod
    def add_to_cart(cls, cashier_id, product_id, qty, unit=None):
        """Add item to cart"""
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        if not unit:
            unit = product.base_unit

        # Check stock
        base_qty = product.convert_to_base(unit, qty)
        if product.stock < base_qty:
            raise ValidationException(
                f'Insufficient stock. Available: {product.stock} {product.base_unit}'
            )

        # Get price with dynamic pricing
        unit_price = product.get_price(unit, qty)
        total = qty * unit_price

        cart = cls.get_cart(cashier_id)

        # Check if item already in cart
        existing_item = None
        for item in cart.items:
            if item['product_id'] == str(product._id) and item['unit'] == unit:
                existing_item = item
                break

        if existing_item:
            existing_item['qty'] += qty
            existing_item['total'] = existing_item['qty'] * existing_item['unit_price']
        else:
            cart.items.append({
                'product_id': str(product._id),
                'product_name': product.name,
                'sku': product.sku,
                'qty': qty,
                'unit': unit,
                'unit_price': unit_price,
                'total': total
            })

        cart.updated_at = datetime.utcnow()
        return cart.to_dict()

    @classmethod
    def remove_from_cart(cls, cashier_id, product_id, unit=None):
        """Remove item from cart"""
        cart = cls.get_cart(cashier_id)
        cart.items = [
            item for item in cart.items 
            if not (item['product_id'] == product_id and (unit is None or item['unit'] == unit))
        ]
        cart.updated_at = datetime.utcnow()
        return cart.to_dict()

    @classmethod
    def update_cart_item(cls, cashier_id, product_id, qty, unit=None):
        """Update cart item quantity"""
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        if not unit:
            unit = product.base_unit

        # Check stock
        base_qty = product.convert_to_base(unit, qty)
        if product.stock < base_qty:
            raise ValidationException('Insufficient stock')

        cart = cls.get_cart(cashier_id)
        for item in cart.items:
            if item['product_id'] == product_id and item['unit'] == unit:
                item['qty'] = qty
                item['unit_price'] = product.get_price(unit, qty)
                item['total'] = qty * item['unit_price']
                break

        cart.updated_at = datetime.utcnow()
        return cart.to_dict()

    @classmethod
    def clear_cart(cls, cashier_id):
        """Clear cart"""
        if cashier_id in cls._carts:
            del cls._carts[cashier_id]
        return {'message': 'Cart cleared'}

    @classmethod
    def apply_discount(cls, cashier_id, discount_amount):
        """Apply discount to cart"""
        cart = cls.get_cart(cashier_id)
        cart.discount_amount = discount_amount
        return cart.to_dict()

    @classmethod
    def checkout(cls, cashier_id, payment_method='cash', customer_id=None, 
                 discount_amount=0, tax_amount=0, amount_paid=0, notes=''):
        """Process checkout"""
        cart = cls.get_cart(cashier_id)

        if not cart.items:
            raise ValidationException('Cart is empty')

        subtotal = cart.subtotal
        total = subtotal - discount_amount + tax_amount

        if amount_paid < total:
            raise ValidationException('Insufficient payment')

        change = amount_paid - total

        # Create sale
        sale_data = {
            'items': cart.items,
            'payment_method': payment_method,
            'discount_amount': discount_amount,
            'tax_amount': tax_amount,
            'customer_id': customer_id,
            'notes': notes
        }

        sale = SalesService.create_sale(sale_data, cashier_id=cashier_id)

        # Get cashier info
        cashier = UserRepository.find_by_id(cashier_id)
        cashier_name = cashier.full_name if cashier else 'Unknown'

        # Create receipt
        receipt = {
            'transaction_code': sale['transaction_code'],
            'store_name': 'Toko Saya',
            'cashier': cashier_name,
            'timestamp': datetime.utcnow().isoformat(),
            'items': cart.items,
            'subtotal': subtotal,
            'discount': discount_amount,
            'tax': tax_amount,
            'total': total,
            'payment_method': payment_method,
            'amount_paid': amount_paid,
            'change': change,
            'customer_id': customer_id
        }

        # Clear cart
        cls.clear_cart(cashier_id)

        return {
            'sale': sale,
            'receipt': receipt
        }

    @classmethod
    def get_cart_summary(cls, cashier_id):
        """Get cart summary"""
        cart = cls.get_cart(cashier_id)
        return {
            'items': cart.items,
            'subtotal': cart.subtotal,
            'total_items': cart.total_items,
            'item_count': len(cart.items)
        }
