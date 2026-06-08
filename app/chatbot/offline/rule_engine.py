"""
Rule Engine - Business rules for offline mode
"""

from app.products.repository import ProductRepository
from app.core.exceptions import NotFoundException


class RuleEngine:
    """Apply business rules to parsed commands"""

    @classmethod
    def process_sale(cls, parsed_data):
        """Process sale intent"""
        product_name = parsed_data.get('product', '')
        qty = parsed_data.get('qty', 1)
        unit = parsed_data.get('unit', 'pcs')
        total_price = parsed_data.get('total_price')

        # Find product by name
        products = ProductRepository.find_by_name(product_name)
        if not products:
            return {
                'success': False,
                'error': f'Product "{product_name}" not found',
                'suggestion': 'Try checking the product name or add it first'
            }

        product = products[0]  # Take first match

        # Calculate price if not provided
        if total_price is None:
            unit_price = product.get_price(unit, qty)
            total_price = unit_price * qty

        # Check stock
        base_qty = product.convert_to_base(unit, qty)
        if product.stock < base_qty:
            return {
                'success': False,
                'error': f'Insufficient stock. Available: {product.stock} {product.base_unit}',
                'product': product.to_dict()
            }
        
        ProductRepository.decrease_stock(
            str(product._id),
            base_qty
        )

        return {
            'success': True,
            'intent': 'sale',
            'product_id': str(product._id),
            'product_name': product.name,
            'qty': qty,
            'unit': unit,
            'unit_price': total_price / qty if qty > 0 else 0,
            'total_price': total_price,
            'stock_after': product.stock - base_qty
        }

    @classmethod
    def process_check_stock(cls, parsed_data):
        """Process check stock intent"""
        product_name = parsed_data.get('product', '')
        products = ProductRepository.find_by_name(product_name)

        if not products:
            return {
                'success': False,
                'error': f'Product "{product_name}" not found'
            }

        product = products[0]
        return {
            'success': True,
            'intent': 'check_stock',
            'product': product.to_dict(),
            'stock': product.stock,
            'min_stock': product.min_stock,
            'status': 'low' if product.stock < product.min_stock else 'ok'
        }

    @classmethod
    def process_check_price(cls, parsed_data):
        """Process check price intent"""
        product_name = parsed_data.get('product', '')
        qty = parsed_data.get('qty', 1)
        unit = parsed_data.get('unit', 'pcs')

        products = ProductRepository.find_by_name(product_name)
        if not products:
            return {
                'success': False,
                'error': f'Product "{product_name}" not found'
            }

        product = products[0]
        price = product.get_price(unit, qty)

        return {
            'success': True,
            'intent': 'check_price',
            'product': product.to_dict(),
            'unit': unit,
            'qty': qty,
            'unit_price': price,
            'total': price * qty
        }

    @classmethod
    def process_add_unit(cls, parsed_data):
        """Process add unit intent"""
        product_name = parsed_data.get('product', '')
        unit = parsed_data.get('unit', '')
        ratio = parsed_data.get('ratio', 1)

        products = ProductRepository.find_by_name(product_name)
        if not products:
            return {
                'success': False,
                'error': f'Product "{product_name}" not found'
            }

        product = products[0]

        # Add unit conversion
        ProductRepository.add_unit_conversion(str(product._id), unit, ratio)

        return {
            'success': True,
            'intent': 'add_unit',
            'product_id': str(product._id),
            'product_name': product.name,
            'new_unit': unit,
            'ratio': ratio,
            'message': f'Unit "{unit}" added to "{product.name}" with ratio {ratio}'
        }
