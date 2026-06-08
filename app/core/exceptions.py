"""
Custom Exceptions and Error Handlers
"""

from flask import jsonify
from marshmallow import ValidationError
from pymongo.errors import DuplicateKeyError, OperationFailure


class APIException(Exception):
    """Base API Exception"""
    status_code = 500
    error_code = 'INTERNAL_ERROR'

    def __init__(self, message='An error occurred', status_code=None, error_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error_code'] = self.error_code
        return rv


class NotFoundException(APIException):
    """Resource not found"""
    status_code = 404
    error_code = 'NOT_FOUND'


class ValidationException(APIException):
    """Validation error"""
    status_code = 400
    error_code = 'VALIDATION_ERROR'


class UnauthorizedException(APIException):
    """Unauthorized access"""
    status_code = 401
    error_code = 'UNAUTHORIZED'


class ForbiddenException(APIException):
    """Forbidden access"""
    status_code = 403
    error_code = 'FORBIDDEN'


class ConflictException(APIException):
    """Resource conflict"""
    status_code = 409
    error_code = 'CONFLICT'


class DatabaseException(APIException):
    """Database error"""
    status_code = 500
    error_code = 'DATABASE_ERROR'


def register_error_handlers(app):
    """Register error handlers with Flask app"""

    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = jsonify({
            'message': 'Validation error',
            'error_code': 'VALIDATION_ERROR',
            'errors': error.messages
        })
        response.status_code = 400
        return response

    @app.errorhandler(DuplicateKeyError)
    def handle_duplicate_key_error(error):
        response = jsonify({
            'message': 'Resource already exists',
            'error_code': 'DUPLICATE_KEY',
            'detail': str(error)
        })
        response.status_code = 409
        return response

    @app.errorhandler(OperationFailure)
    def handle_operation_failure(error):
        response = jsonify({
            'message': 'Database operation failed',
            'error_code': 'DATABASE_ERROR',
            'detail': str(error)
        })
        response.status_code = 500
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        response = jsonify({
            'message': 'Endpoint not found',
            'error_code': 'NOT_FOUND'
        })
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def handle_internal_error(error):
        response = jsonify({
            'message': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        })
        response.status_code = 500
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        response = jsonify({
            'message': 'An unexpected error occurred',
            'error_code': 'UNKNOWN_ERROR',
            'detail': str(error) if app.debug else None
        })
        response.status_code = 500
        return response
