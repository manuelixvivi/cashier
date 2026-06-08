"""
Unit Conversion Engine
"""

from app.products.repository import ProductRepository
from app.core.exceptions import NotFoundException


class ConversionEngine:
    """Unit conversion engine"""

    @classmethod
    def convert(cls, product_id, from_unit, to_unit, qty):
        """Convert quantity between units"""
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        # Convert to base unit first
        base_qty = cls._to_base(product, from_unit, qty)
        # Convert from base to target
        result = cls._from_base(product, to_unit, base_qty)

        return {
            'product_id': product_id,
            'from_unit': from_unit,
            'to_unit': to_unit,
            'input_qty': qty,
            'base_qty': base_qty,
            'result_qty': round(result, 4)
        }

    @classmethod
    def _to_base(cls, product, unit, qty):
        """Convert to base unit"""
        if unit == product.base_unit:
            return qty
        ratio = product.conversions.get(unit)
        if ratio is None:
            raise NotFoundException(f"Conversion for unit '{unit}' not found")
        return qty * ratio

    @classmethod
    def _from_base(cls, product, unit, base_qty):
        """Convert from base unit"""
        if unit == product.base_unit:
            return base_qty
        ratio = product.conversions.get(unit)
        if ratio is None:
            raise NotFoundException(f"Conversion for unit '{unit}' not found")
        return base_qty / ratio

    @classmethod
    def get_available_units(cls, product_id):
        """Get all available units for product"""
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise NotFoundException('Product not found')

        units = [product.base_unit]
        units.extend(product.conversions.keys())

        return {
            'product_id': product_id,
            'base_unit': product.base_unit,
            'available_units': units,
            'conversions': product.conversions
        }
