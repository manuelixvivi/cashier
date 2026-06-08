"""
Flask Extensions Initialization
Centralized extension instances for App Factory Pattern
"""

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from celery import Celery


# Initialize extensions without app context
jwt = JWTManager()
bcrypt = Bcrypt()
mongo = PyMongo()

celery = Celery(
    'pos_ai_backend',
    include=[
        'app.tasks.stock_monitor',
        'app.tasks.report_scheduler',
        'app.tasks.forecast_scheduler',
    ]
)
