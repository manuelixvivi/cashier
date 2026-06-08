"""
Purchase Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.response import APIResponse
from app.purchases.service import PurchaseService

purchases_bp = Blueprint('purchases', __name__)


@purchases_bp.route('/', methods=['POST'])
@jwt_required()
def create_po():
    data = request.get_json()
    result = PurchaseService.create_po(data, created_by=get_jwt_identity())
    return APIResponse.success(data=result, message='Purchase order created', status_code=201)


@purchases_bp.route('/', methods=['GET'])
@jwt_required()
def list_pos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    result = PurchaseService.list_pos(page=page, per_page=per_page, status=status)
    return APIResponse.paginated(
        data=result['purchase_orders'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@purchases_bp.route('/<po_id>', methods=['GET'])
@jwt_required()
def get_po(po_id):
    result = PurchaseService.get_po(po_id)
    return APIResponse.success(data=result)


@purchases_bp.route('/<po_id>/receive', methods=['POST'])
@jwt_required()
def receive_po(po_id):
    result = PurchaseService.receive_po(po_id, created_by=get_jwt_identity())
    return APIResponse.success(data=result)


@purchases_bp.route('/<po_id>/status', methods=['PUT'])
@jwt_required()
def update_po_status(po_id):
    data = request.get_json()
    result = PurchaseService.update_po_status(po_id, data['status'])
    return APIResponse.success(data=result)
