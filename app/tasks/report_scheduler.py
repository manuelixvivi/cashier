"""
Report Scheduler Tasks
"""

from celery import shared_task
from app.reports.daily_report import DailyReport
from app.notifications.service import NotificationService


@shared_task
def generate_daily_report():
    """Generate daily report"""
    from datetime import datetime
    report = DailyReport.generate()

    NotificationService.create_notification(
        title='Daily Report Generated',
        message=f"Daily report for {report['date']} is ready. Total sales: Rp {report['sales_summary'].get('total_sales', 0):,.0f}",
        type='info',
        link='/reports/daily'
    )

    return report
