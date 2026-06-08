"""
POS AI Backend - Application Factory Entry Point
Enterprise-grade Point of Sale system with AI Chatbot capabilities
"""

import os
from datetime import datetime

from flask import Flask, jsonify
from config.config import Config
from config.database import Database
from app.core.extensions import jwt, bcrypt, mongo, celery
from app.core.exceptions import register_error_handlers
from app.core.middleware import register_middleware
from app.core.response import APIResponse


def create_app(config_class=Config):
    """
    Application Factory Pattern - Creates Flask app instance
    with all extensions and blueprints registered
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    initialize_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register middleware
    register_middleware(app)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return APIResponse.success(
            data={
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': '1.0.0',
                'environment': app.config.get('ENV', 'development')
            }
        )

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'name': 'POS AI Backend API',
            'version': '1.0.0',
            'description': 'Enterprise POS System with AI Chatbot',
            'endpoints': {
                'health': '/health',
                'api_docs': '/api/v1/docs',
                'auth': '/api/v1/auth',
                'products': '/api/v1/products',
                'pos': '/api/v1/pos',
                'chatbot': '/api/v1/chatbot',
                'reports': '/api/v1/reports',
                'analytics': '/api/v1/analytics',
                'forecasting': '/api/v1/forecasting'
            }
        })

    return app


def initialize_extensions(app):
    """Initialize Flask extensions with app context"""
    jwt.init_app(app)
    bcrypt.init_app(app)
    mongo.init_app(app)
    celery.conf.update(app.config)

    # Initialize database connection
    Database.initialize(app)


def register_blueprints(app):
    """Register all Flask Blueprints"""
    # Auth
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # Users
    from app.users.routes import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')

    # Roles
    from app.roles.routes import roles_bp
    app.register_blueprint(roles_bp, url_prefix='/api/v1/roles')

    # Products
    from app.products.routes import products_bp
    app.register_blueprint(products_bp, url_prefix='/api/v1/products')

    # Inventory
    from app.inventory.routes import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/api/v1/inventory')

    # Suppliers
    from app.suppliers.routes import suppliers_bp
    app.register_blueprint(suppliers_bp, url_prefix='/api/v1/suppliers')

    # Customers
    from app.customers.routes import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/api/v1/customers')

    # Purchases
    from app.purchases.routes import purchases_bp
    app.register_blueprint(purchases_bp, url_prefix='/api/v1/purchases')

    # Sales
    from app.sales.routes import sales_bp
    app.register_blueprint(sales_bp, url_prefix='/api/v1/sales')

    # POS
    from app.pos.routes import pos_bp
    app.register_blueprint(pos_bp, url_prefix='/api/v1/pos')

    # Pricing
    from app.pricing.routes import pricing_bp
    app.register_blueprint(pricing_bp, url_prefix='/api/v1/pricing')

    # Units
    from app.units.routes import units_bp
    app.register_blueprint(units_bp, url_prefix='/api/v1/units')

    # Chatbot
    from app.chatbot.routes import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/api/v1/chatbot')

    # Reports
    from app.reports.routes import reports_bp
    app.register_blueprint(reports_bp, url_prefix='/api/v1/reports')

    # Analytics
    from app.analytics.routes import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics')

    # Forecasting
    from app.forecasting.routes import forecasting_bp
    app.register_blueprint(forecasting_bp, url_prefix='/api/v1/forecasting')

    # Notifications
    from app.notifications.routes import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/api/v1/notifications')

    # Audit
    from app.audit.routes import audit_bp
    app.register_blueprint(audit_bp, url_prefix='/api/v1/audit')

    # Settings
    from app.settings.routes import settings_bp
    app.register_blueprint(settings_bp, url_prefix='/api/v1/settings')


# Create Celery app instance
def make_celery(app=None):
    """Create Celery instance with Flask app context"""
    app = app or create_app()
    celery_app = celery
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
