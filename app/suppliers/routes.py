"""
Supplier Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.suppliers.service import SupplierService

suppliers_bp = Blueprint('suppliers', __name__)


@suppliers_bp.route('/', methods=['POST'])
@jwt_required()
def create_supplier():
    data = request.get_json()
    result = SupplierService.create_supplier(data)
    return APIResponse.success(data=result, message='Supplier created', status_code=201)


@suppliers_bp.route('/', methods=['GET'])
@jwt_required()
def list_suppliers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    result = SupplierService.list_suppliers(page=page, per_page=per_page)
    return APIResponse.paginated(
        data=result['suppliers'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@suppliers_bp.route('/<supplier_id>', methods=['GET'])
@jwt_required()
def get_supplier(supplier_id):
    result = SupplierService.get_supplier(supplier_id)
    return APIResponse.success(data=result)


@suppliers_bp.route('/<supplier_id>', methods=['PUT'])
@jwt_required()
def update_supplier(supplier_id):
    data = request.get_json()
    result = SupplierService.update_supplier(supplier_id, data)
    return APIResponse.success(data=result, message='Supplier updated')


@suppliers_bp.route('/<supplier_id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(supplier_id):
    SupplierService.delete_supplier(supplier_id)
    return APIResponse.success(message='Supplier deleted')
