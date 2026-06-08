"""
Flask Middleware
Request/Response interceptors
"""

import time
import uuid
from flask import request, g, current_app
from datetime import datetime


def register_middleware(app):
    """Register all middleware with Flask app"""

    @app.before_request
    def before_request():
        """Execute before each request"""
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()
        g.request_time = datetime.utcnow()

        current_app.logger.info(
            f"Request started",
            extra={
                'request_id': g.request_id,
                'method': request.method,
                'path': request.path,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string if request.user_agent else None
            }
        )

    @app.after_request
    def after_request(response):
        """Execute after each request"""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            response.headers['X-Request-ID'] = g.request_id
            response.headers['X-Response-Time'] = f"{duration:.3f}s"

            current_app.logger.info(
                f"Request completed",
                extra={
                    'request_id': g.request_id,
                    'status_code': response.status_code,
                    'duration_ms': round(duration * 1000, 2)
                }
            )

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response

    @app.teardown_appcontext
    def teardown_appcontext(exception=None):
        """Cleanup after request"""
        pass
