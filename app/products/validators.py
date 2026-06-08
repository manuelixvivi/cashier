"""
Product Validators
"""

import re
from app.core.exceptions import ValidationException


class ProductValidator:
    """Product validation utilities"""

    @staticmethod
    def validate_sku(sku):
        if not sku or len(sku) < 1 or len(sku) > 50:
            raise ValidationException('SKU must be between 1 and 50 characters')
        if not re.match(r'^[A-Za-z0-9\-_]+$', sku):
            raise ValidationException('SKU can only contain letters, numbers, hyphens, and underscores')

    @staticmethod
    def validate_barcode(barcode):
        if not barcode:
            return
        if len(barcode) < 8 or len(barcode) > 100:
            raise ValidationException('Barcode must be between 8 and 100 characters')
        if not barcode.isdigit():
            raise ValidationException('Barcode must contain only digits')

    @staticmethod
    def validate_pricing_tiers(tiers):
        if not tiers:
            return
        sorted_tiers = sorted(tiers, key=lambda x: x.get('min_qty', 0))
        for i, tier in enumerate(sorted_tiers):
            if tier.get('min_qty', 0) < 0:
                raise ValidationException('min_qty must be non-negative')
            if tier.get('price', 0) < 0:
                raise ValidationException('price must be non-negative')
            if i > 0 and tier['min_qty'] == sorted_tiers[i-1]['min_qty']:
                raise ValidationException(f"Duplicate min_qty: {tier['min_qty']}")

    @staticmethod
    def validate_unit_conversion(base_unit, conversions):
        if base_unit in conversions:
            raise ValidationException('Conversion unit cannot be the same as base unit')
        for unit, ratio in conversions.items():
            if ratio <= 0:
                raise ValidationException(f"Conversion ratio for '{unit}' must be positive")

    @staticmethod
    def validate_stock_levels(stock, min_stock, max_stock):
        if min_stock < 0:
            raise ValidationException('min_stock must be non-negative')
        if max_stock < 0:
            raise ValidationException('max_stock must be non-negative')
        if max_stock > 0 and min_stock > max_stock:
            raise ValidationException('min_stock cannot be greater than max_stock')
        if stock < 0:
            raise ValidationException('stock must be non-negative')
