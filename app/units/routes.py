"""
Unit Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.units.unit_service import UnitService

units_bp = Blueprint('units', __name__)


@units_bp.route('/convert', methods=['POST'])
@jwt_required()
def convert():
    """Convert between units"""
    data = request.get_json()
    result = UnitService.convert(
        product_id=data['product_id'],
        from_unit=data['from_unit'],
        to_unit=data['to_unit'],
        qty=data['qty']
    )
    return APIResponse.success(data=result)


@units_bp.route('/<product_id>', methods=['GET'])
@jwt_required()
def get_units(product_id):
    """Get available units for product"""
    result = UnitService.get_units(product_id)
    return APIResponse.success(data=result)
