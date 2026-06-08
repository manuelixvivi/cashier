"""
Unit Service
"""

from app.units.conversion_engine import ConversionEngine


class UnitService:
    """Unit service facade"""

    @classmethod
    def convert(cls, product_id, from_unit, to_unit, qty):
        return ConversionEngine.convert(product_id, from_unit, to_unit, qty)

    @classmethod
    def get_units(cls, product_id):
        return ConversionEngine.get_available_units(product_id)
