"""
Customer Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.customers.service import CustomerService

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    result = CustomerService.create_customer(data)
    return APIResponse.success(data=result, message='Customer created', status_code=201)


@customers_bp.route('/', methods=['GET'])
@jwt_required()
def list_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search')
    result = CustomerService.list_customers(page=page, per_page=per_page, search=search)
    return APIResponse.paginated(
        data=result['customers'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@customers_bp.route('/<customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    result = CustomerService.get_customer(customer_id)
    return APIResponse.success(data=result)


@customers_bp.route('/phone/<phone>', methods=['GET'])
@jwt_required()
def get_customer_by_phone(phone):
    result = CustomerService.get_customer_by_phone(phone)
    return APIResponse.success(data=result)


@customers_bp.route('/<customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    data = request.get_json()
    result = CustomerService.update_customer(customer_id, data)
    return APIResponse.success(data=result, message='Customer updated')


@customers_bp.route('/<customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    CustomerService.delete_customer(customer_id)
    return APIResponse.success(message='Customer deleted')
