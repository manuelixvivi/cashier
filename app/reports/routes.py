"""
Report Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.reports.daily_report import DailyReport
from app.reports.weekly_report import WeeklyReport
from app.reports.monthly_report import MonthlyReport
from app.reports.yearly_report import YearlyReport
from app.reports.profit_report import ProfitReport

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/daily', methods=['GET'])
@jwt_required()
def daily_report():
    """Get daily report"""
    from datetime import datetime
    date_str = request.args.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    result = DailyReport.generate(date)
    return APIResponse.success(data=result)


@reports_bp.route('/weekly', methods=['GET'])
@jwt_required()
def weekly_report():
    """Get weekly report"""
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)
    result = WeeklyReport.generate(year=year, week=week)
    return APIResponse.success(data=result)


@reports_bp.route('/monthly', methods=['GET'])
@jwt_required()
def monthly_report():
    """Get monthly report"""
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    result = MonthlyReport.generate(year=year, month=month)
    return APIResponse.success(data=result)


@reports_bp.route('/yearly', methods=['GET'])
@jwt_required()
def yearly_report():
    """Get yearly report"""
    year = request.args.get('year', type=int)
    result = YearlyReport.generate(year=year)
    return APIResponse.success(data=result)


@reports_bp.route('/profit', methods=['GET'])
@jwt_required()
def profit_report():
    """Get profit report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    result = ProfitReport.generate(start_date=start_date, end_date=end_date)
    return APIResponse.success(data=result)
