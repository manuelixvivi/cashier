"""
Sales Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.response import APIResponse
from app.sales.service import SalesService

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/', methods=['POST'])
@jwt_required()
def create_sale():
    data = request.get_json()
    result = SalesService.create_sale(data, cashier_id=get_jwt_identity())
    return APIResponse.success(data=result, message='Sale created', status_code=201)


@sales_bp.route('/', methods=['GET'])
@jwt_required()
def list_sales():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    result = SalesService.list_sales(
        page=page, per_page=per_page,
        start_date=start_date, end_date=end_date
    )
    return APIResponse.paginated(
        data=result['sales'],
        page=result['page'],
        per_page=result['per_page'],
        total=result['total'],
        total_pages=result['total_pages']
    )


@sales_bp.route('/<sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    result = SalesService.get_sale(sale_id)
    return APIResponse.success(data=result)


@sales_bp.route('/code/<code>', methods=['GET'])
@jwt_required()
def get_sale_by_code(code):
    result = SalesService.get_sale_by_code(code)
    return APIResponse.success(data=result)


@sales_bp.route('/<sale_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_sale(sale_id):
    data = request.get_json() or {}
    result = SalesService.cancel_sale(sale_id, reason=data.get('reason', ''))
    return APIResponse.success(data=result)


@sales_bp.route('/daily-summary', methods=['GET'])
@jwt_required()
def daily_summary():
    from datetime import datetime
    date_str = request.args.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    result = SalesService.get_daily_summary(date)
    return APIResponse.success(data=result)
