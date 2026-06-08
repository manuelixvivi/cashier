"""
POS Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.response import APIResponse
from app.pos.service import POSService

pos_bp = Blueprint('pos', __name__)


@pos_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get current cart"""
    cashier_id = get_jwt_identity()
    result = POSService.get_cart_summary(cashier_id)
    return APIResponse.success(data=result)


@pos_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    cashier_id = get_jwt_identity()
    data = request.get_json()
    result = POSService.add_to_cart(
        cashier_id=cashier_id,
        product_id=data['product_id'],
        qty=data['qty'],
        unit=data.get('unit')
    )
    return APIResponse.success(data=result, message='Item added to cart')


@pos_bp.route('/cart/remove', methods=['POST'])
@jwt_required()
def remove_from_cart():
    """Remove item from cart"""
    cashier_id = get_jwt_identity()
    data = request.get_json()
    result = POSService.remove_from_cart(
        cashier_id=cashier_id,
        product_id=data['product_id'],
        unit=data.get('unit')
    )
    return APIResponse.success(data=result, message='Item removed from cart')


@pos_bp.route('/cart/update', methods=['POST'])
@jwt_required()
def update_cart_item():
    """Update cart item quantity"""
    cashier_id = get_jwt_identity()
    data = request.get_json()
    result = POSService.update_cart_item(
        cashier_id=cashier_id,
        product_id=data['product_id'],
        qty=data['qty'],
        unit=data.get('unit')
    )
    return APIResponse.success(data=result, message='Cart updated')


@pos_bp.route('/cart/clear', methods=['POST'])
@jwt_required()
def clear_cart():
    """Clear cart"""
    cashier_id = get_jwt_identity()
    result = POSService.clear_cart(cashier_id)
    return APIResponse.success(data=result)


@pos_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """Process checkout"""
    cashier_id = get_jwt_identity()
    data = request.get_json()
    result = POSService.checkout(
        cashier_id=cashier_id,
        payment_method=data.get('payment_method', 'cash'),
        customer_id=data.get('customer_id'),
        discount_amount=data.get('discount_amount', 0),
        tax_amount=data.get('tax_amount', 0),
        amount_paid=data.get('amount_paid', 0),
        notes=data.get('notes', '')
    )
    return APIResponse.success(data=result, message='Checkout successful')
