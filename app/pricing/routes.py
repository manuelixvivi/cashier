"""
Pricing Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.pricing.pricing_service import PricingService

pricing_bp = Blueprint('pricing', __name__)


@pricing_bp.route('/calculate', methods=['POST'])
@jwt_required()
def calculate_price():
    """Calculate price for product"""
    data = request.get_json()
    result = PricingService.get_price(
        product_id=data['product_id'],
        unit=data.get('unit', 'pcs'),
        qty=data['qty'],
        customer_level=data.get('customer_level')
    )
    return APIResponse.success(data=result)


@pricing_bp.route('/bulk', methods=['POST'])
@jwt_required()
def bulk_pricing():
    """Get bulk pricing"""
    data = request.get_json()
    result = PricingService.get_bulk_pricing(
        product_id=data['product_id'],
        quantities=data['quantities']
    )
    return APIResponse.success(data=result)
