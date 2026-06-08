"""
Forecasting Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.forecasting.forecast_service import ForecastService

forecasting_bp = Blueprint('forecasting', __name__)


@forecasting_bp.route('/sales', methods=['GET'])
@jwt_required()
def sales_forecast():
    """Get sales forecast"""
    method = request.args.get('method', 'moving_average')
    days = request.args.get('days', 30, type=int)
    result = ForecastService.sales_forecast(method=method, days=days)
    return APIResponse.success(data=result)


@forecasting_bp.route('/stock/<product_id>', methods=['GET'])
@jwt_required()
def stock_forecast(product_id):
    """Get stock runout forecast"""
    days = request.args.get('days', 30, type=int)
    result = ForecastService.stock_forecast(product_id, days=days)
    return APIResponse.success(data=result)


@forecasting_bp.route('/demand/<product_id>', methods=['GET'])
@jwt_required()
def demand_forecast(product_id):
    """Get product demand forecast"""
    method = request.args.get('method', 'prophet')
    days = request.args.get('days', 14, type=int)
    result = ForecastService.product_demand_forecast(product_id, method=method, days=days)
    return APIResponse.success(data=result)


@forecasting_bp.route('/methods', methods=['GET'])
@jwt_required()
def available_methods():
    """Get available forecasting methods"""
    result = ForecastService.get_available_methods()
    return APIResponse.success(data={'methods': result})
