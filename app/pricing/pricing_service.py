"""
Pricing Service
"""

from app.pricing.pricing_engine import PricingEngine


class PricingService:
    """Pricing service facade"""

    @classmethod
    def get_price(cls, product_id, unit, qty, customer_level=None):
        return PricingEngine.calculate_price(product_id, unit, qty, customer_level)

    @classmethod
    def get_bulk_pricing(cls, product_id, quantities):
        return PricingEngine.bulk_pricing(product_id, quantities)
