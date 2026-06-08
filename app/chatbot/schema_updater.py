"""
Schema Updater - Dynamic schema updates from AI commands
"""

from app.products.repository import ProductRepository
from app.core.exceptions import NotFoundException


class SchemaUpdater:
    """Update product schema dynamically based on AI commands"""

    @classmethod
    def add_unit_to_product(cls, product_name, unit, ratio=1):
        """Add new unit to product dynamically"""
        products = ProductRepository.find_by_name(product_name)
        if not products:
            # Create product if not exists (optional)
            return {
                'success': False,
                'error': f'Product "{product_name}" not found. Cannot add unit.'
            }

        product = products[0]
        ProductRepository.add_unit_conversion(str(product._id), unit, ratio)

        return {
            'success': True,
            'message': f'Added unit "{unit}" to "{product.name}"',
            'product': product.to_dict()
        }

    @classmethod
    def add_custom_field(cls, product_name, field_name, field_value):
        """Add custom field to product"""
        products = ProductRepository.find_by_name(product_name)
        if not products:
            return {
                'success': False,
                'error': f'Product "{product_name}" not found'
            }

        product = products[0]
        ProductRepository.add_dynamic_field(str(product._id), field_name, field_value)

        return {
            'success': True,
            'message': f'Added field "{field_name}" to "{product.name}"',
            'product': product.to_dict()
        }

    @classmethod
    def update_pricing_rule(cls, product_name, unit, tiers):
        """Update pricing rule for product"""
        products = ProductRepository.find_by_name(product_name)
        if not products:
            return {
                'success': False,
                'error': f'Product "{product_name}" not found'
            }

        product = products[0]

        # Validate unit exists
        if unit != product.base_unit and unit not in product.conversions:
            return {
                'success': False,
                'error': f'Unit "{unit}" not found. Add unit conversion first.'
            }

        # Remove existing rule for this unit
        from config.database import get_db
        db = get_db()
        db[ProductRepository.COLLECTION].update_one(
            {'_id': product._id},
            {'$pull': {'pricing_rules': {'unit': unit}}}
        )

        # Add new rule
        pricing_rule = {'unit': unit, 'tiers': tiers}
        ProductRepository.add_pricing_rule(str(product._id), pricing_rule)

        return {
            'success': True,
            'message': f'Updated pricing for "{unit}" on "{product.name}"',
            'product': product.to_dict()
        }
