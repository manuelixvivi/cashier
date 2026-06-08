"""
Product Models with Dynamic Schema Support
"""

from datetime import datetime
from bson import ObjectId


class Product:
    """
    Product model with dynamic schema support
    Supports multiple units, pricing tiers, and custom fields
    """
    COLLECTION = 'products'

    def __init__(self, name, sku, category='', description='', 
                 barcode='', base_unit='pcs', conversions=None,
                 pricing_rules=None, cost_price=0, stock=0,
                 min_stock=0, max_stock=0, supplier_id=None,
                 is_active=True, custom_fields=None, _id=None,
                 created_at=None, updated_at=None):
        self._id = _id or ObjectId()
        self.name = name
        self.sku = sku
        self.category = category
        self.description = description
        self.barcode = barcode
        self.base_unit = base_unit
        self.conversions = conversions or {}  # {unit: ratio_to_base}
        self.pricing_rules = pricing_rules or []
        self.cost_price = cost_price
        self.stock = stock
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.supplier_id = supplier_id
        self.is_active = is_active
        self.custom_fields = custom_fields or {}  # Dynamic fields
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'sku': self.sku,
            'category': self.category,
            'description': self.description,
            'barcode': self.barcode,
            'base_unit': self.base_unit,
            'conversions': self.conversions,
            'pricing_rules': self.pricing_rules,
            'cost_price': self.cost_price,
            'stock': self.stock,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'supplier_id': str(self.supplier_id) if self.supplier_id else None,
            'is_active': self.is_active,
            'custom_fields': self.custom_fields,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            _id=data.get('_id'),
            name=data.get('name'),
            sku=data.get('sku'),
            category=data.get('category', ''),
            description=data.get('description', ''),
            barcode=data.get('barcode', ''),
            base_unit=data.get('base_unit', 'pcs'),
            conversions=data.get('conversions', {}),
            pricing_rules=data.get('pricing_rules', []),
            cost_price=data.get('cost_price', 0),
            stock=data.get('stock', 0),
            min_stock=data.get('min_stock', 0),
            max_stock=data.get('max_stock', 0),
            supplier_id=data.get('supplier_id'),
            is_active=data.get('is_active', True),
            custom_fields=data.get('custom_fields', {}),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def get_price(self, unit, qty=1):
        """Get price for unit and quantity (dynamic pricing)"""
        for rule in self.pricing_rules:
            if rule.get('unit') == unit:
                tiers = rule.get('tiers', [])
                tiers = sorted(tiers, key=lambda x: x.get('min_qty', 0), reverse=True)
                for tier in tiers:
                    if qty >= tier.get('min_qty', 0):
                        return tier.get('price', 0)

        if unit == self.base_unit:
            return self.cost_price

        ratio = self.conversions.get(unit, 1)
        return self.cost_price * ratio

    def convert_to_base(self, unit, qty):
        """Convert quantity to base unit"""
        if unit == self.base_unit:
            return qty
        ratio = self.conversions.get(unit, 1)
        return qty * ratio

    def convert_from_base(self, unit, base_qty):
        """Convert from base unit to target unit"""
        if unit == self.base_unit:
            return base_qty
        ratio = self.conversions.get(unit, 1)
        return base_qty / ratio


class ProductCategory:
    """Product category model"""
    COLLECTION = 'product_categories'

    def __init__(self, name, description='', parent_id=None, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'description': self.description,
            'parent_id': str(self.parent_id) if self.parent_id else None,
            'created_at': self.created_at.isoformat()
        }
