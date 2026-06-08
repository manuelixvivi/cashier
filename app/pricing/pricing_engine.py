"""
Pricing Engine - Dynamic pricing calculation
"""

from app.products.repository import ProductRepository
from app.core.exceptions import NotFoundException


class PricingEngine:
    """Dynamic pricing calculation engine"""

    @classmethod
    def calculate_price(cls, product_id, unit, qty, customer_level=None):
        """Calculate final price with all rules applied"""
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        # Base price from dynamic pricing tiers
        base_price = product.get_price(unit, qty)

        # Apply customer level discount
        discount = 0
        if customer_level:
            discount = cls._get_customer_discount(customer_level)

        final_price = base_price * (1 - discount)

        return {
            'product_id': product_id,
            'unit': unit,
            'quantity': qty,
            'base_price': base_price,
            'customer_level': customer_level,
            'discount_rate': discount,
            'discount_amount': base_price * discount * qty,
            'final_unit_price': final_price,
            'total': final_price * qty
        }

    @classmethod
    def _get_customer_discount(cls, level):
        """Get discount rate by customer level"""
        discounts = {
            'regular': 0,
            'silver': 0.05,
            'gold': 0.10,
            'platinum': 0.15
        }
        return discounts.get(level, 0)

    @classmethod
    def bulk_pricing(cls, product_id, quantities):
        """Calculate pricing for multiple quantities"""
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        results = []
        for qty_info in quantities:
            unit = qty_info.get('unit', product.base_unit)
            qty = qty_info['qty']
            price = product.get_price(unit, qty)
            results.append({
                'qty': qty,
                'unit': unit,
                'unit_price': price,
                'total': price * qty
            })

        return results
