"""
Inventory Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.response import APIResponse
from app.inventory.service import InventoryService

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/goods-receipt', methods=['POST'])
@jwt_required()
def goods_receipt():
    data = request.get_json()
    result = InventoryService.goods_receipt(
        product_id=data['product_id'],
        quantity=data['quantity'],
        unit=data.get('unit', 'pcs'),
        reference_id=data.get('reference_id'),
        reference_type=data.get('reference_type'),
        notes=data.get('notes', ''),
        created_by=get_jwt_identity(),
        location=data.get('location', 'default')
    )
    return APIResponse.success(data=result, message='Goods receipt recorded')


@inventory_bp.route('/stock-out', methods=['POST'])
@jwt_required()
def stock_out():
    data = request.get_json()
    result = InventoryService.stock_out(
        product_id=data['product_id'],
        quantity=data['quantity'],
        unit=data.get('unit', 'pcs'),
        reference_id=data.get('reference_id'),
        reference_type=data.get('reference_type'),
        notes=data.get('notes', ''),
        created_by=get_jwt_identity(),
        location=data.get('location', 'default')
    )
    return APIResponse.success(data=result, message='Stock out recorded')


@inventory_bp.route('/adjustment', methods=['POST'])
@jwt_required()
def stock_adjustment():
    data = request.get_json()
    result = InventoryService.stock_adjustment(
        product_id=data['product_id'],
        new_qty=data['new_qty'],
        unit=data.get('unit', 'pcs'),
        reason=data.get('reason', ''),
        created_by=get_jwt_identity(),
        location=data.get('location', 'default')
    )
    return APIResponse.success(data=result, message='Stock adjusted')


@inventory_bp.route('/opname', methods=['POST'])
@jwt_required()
def stock_opname():
    data = request.get_json()
    result = InventoryService.stock_opname(
        product_id=data['product_id'],
        physical_qty=data['physical_qty'],
        unit=data.get('unit', 'pcs'),
        notes=data.get('notes', ''),
        created_by=get_jwt_identity()
    )
    return APIResponse.success(data=result, message='Stock opname recorded')


@inventory_bp.route('/transfer', methods=['POST'])
@jwt_required()
def stock_transfer():
    data = request.get_json()
    result = InventoryService.stock_transfer(
        product_id=data['product_id'],
        from_location=data['from_location'],
        to_location=data['to_location'],
        quantity=data['quantity'],
        unit=data.get('unit', 'pcs'),
        notes=data.get('notes', ''),
        created_by=get_jwt_identity()
    )
    return APIResponse.success(data=result, message='Stock transfer created')


@inventory_bp.route('/transfer/<transfer_id>/complete', methods=['POST'])
@jwt_required()
def complete_transfer(transfer_id):
    result = InventoryService.complete_transfer(transfer_id, created_by=get_jwt_identity())
    return APIResponse.success(data=result, message='Transfer completed')


@inventory_bp.route('/movements/<product_id>', methods=['GET'])
@jwt_required()
def get_movements(product_id):
    limit = request.args.get('limit', 50, type=int)
    result = InventoryService.get_product_movements(product_id, limit)
    return APIResponse.success(data=result)


@inventory_bp.route('/opnames/<product_id>', methods=['GET'])
@jwt_required()
def get_opnames(product_id):
    limit = request.args.get('limit', 20, type=int)
    result = InventoryService.get_product_opnames(product_id, limit)
    return APIResponse.success(data=result)
