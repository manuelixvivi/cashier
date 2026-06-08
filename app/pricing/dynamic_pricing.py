"""
Dynamic Pricing Rules
"""

from datetime import datetime, time


class DynamicPricingRules:
    """Advanced dynamic pricing rules"""

    @staticmethod
    def time_based_discount(current_time=None):
        """Discount based on time of day"""
        if current_time is None:
            current_time = datetime.now().time()

        # Morning discount (6-9 AM)
        if time(6, 0) <= current_time <= time(9, 0):
            return 0.05
        # Late night discount (10 PM - 6 AM)
        if current_time >= time(22, 0) or current_time <= time(6, 0):
            return 0.10
        return 0

    @staticmethod
    def quantity_discount(qty, tiers=None):
        """Discount based on quantity tiers"""
        if tiers is None:
            tiers = [
                (10, 0.05),
                (50, 0.10),
                (100, 0.15)
            ]

        for threshold, discount in sorted(tiers, reverse=True):
            if qty >= threshold:
                return discount
        return 0

    @staticmethod
    def bundle_discount(items, bundle_rules):
        """Discount for bundled items"""
        # bundle_rules: [{'products': ['A', 'B'], 'discount': 0.10}]
        total_discount = 0
        for rule in bundle_rules:
            if all(item in [i['product_id'] for i in items] for item in rule['products']):
                total_discount += rule['discount']
        return min(total_discount, 0.50)  # Max 50% discount
