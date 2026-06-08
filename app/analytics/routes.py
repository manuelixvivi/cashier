"""
Analytics Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.analytics.sales_analytics import SalesAnalytics
from app.analytics.inventory_analytics import InventoryAnalytics
from app.analytics.customer_analytics import CustomerAnalytics
from app.analytics.dashboard_service import DashboardService

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """Get dashboard data"""
    result = DashboardService.get_dashboard_data()
    return APIResponse.success(data=result)


@analytics_bp.route('/top-products', methods=['GET'])
@jwt_required()
def top_products():
    """Get top selling products"""
    limit = request.args.get('limit', 10, type=int)
    days = request.args.get('days', 30, type=int)
    result = SalesAnalytics.top_products(limit=limit, days=days)
    return APIResponse.success(data=result)


@analytics_bp.route('/slow-products', methods=['GET'])
@jwt_required()
def slow_products():
    """Get slow moving products"""
    days = request.args.get('days', 30, type=int)
    result = SalesAnalytics.slow_moving_products(days=days)
    return APIResponse.success(data=result)


@analytics_bp.route('/sales-trend', methods=['GET'])
@jwt_required()
def sales_trend():
    """Get sales trend"""
    days = request.args.get('days', 30, type=int)
    result = SalesAnalytics.sales_trend(days=days)
    return APIResponse.success(data=result)


@analytics_bp.route('/hourly-distribution', methods=['GET'])
@jwt_required()
def hourly_distribution():
    """Get hourly sales distribution"""
    days = request.args.get('days', 7, type=int)
    result = SalesAnalytics.hourly_distribution(days=days)
    return APIResponse.success(data=result)


@analytics_bp.route('/stock-turnover', methods=['GET'])
@jwt_required()
def stock_turnover():
    """Get stock turnover"""
    days = request.args.get('days', 30, type=int)
    result = InventoryAnalytics.stock_turnover(days=days)
    return APIResponse.success(data=result)


@analytics_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def low_stock_alert():
    """Get low stock alerts"""
    result = InventoryAnalytics.low_stock_alert()
    return APIResponse.success(data=result)


@analytics_bp.route('/stock-value', methods=['GET'])
@jwt_required()
def stock_value():
    """Get total stock value"""
    result = InventoryAnalytics.stock_value()
    return APIResponse.success(data=result)


@analytics_bp.route('/top-customers', methods=['GET'])
@jwt_required()
def top_customers():
    """Get top customers"""
    limit = request.args.get('limit', 10, type=int)
    days = request.args.get('days', 30, type=int)
    result = CustomerAnalytics.top_customers(limit=limit, days=days)
    return APIResponse.success(data=result)


@analytics_bp.route('/customer-segments', methods=['GET'])
@jwt_required()
def customer_segments():
    """Get customer segments"""
    result = CustomerAnalytics.customer_segments()
    return APIResponse.success(data=result)
