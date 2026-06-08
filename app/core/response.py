"""
Standardized API Response Formatter
"""

from flask import jsonify


class APIResponse:
    """Standardized API Response wrapper"""

    @staticmethod
    def success(data=None, message='Success', status_code=200, meta=None):
        """Create success response"""
        response = {
            'success': True,
            'message': message,
            'data': data or {}
        }
        if meta:
            response['meta'] = meta
        return jsonify(response), status_code

    @staticmethod
    def error(message='Error occurred', error_code='ERROR', status_code=400, errors=None):
        """Create error response"""
        response = {
            'success': False,
            'message': message,
            'error_code': error_code
        }
        if errors:
            response['errors'] = errors
        return jsonify(response), status_code

    @staticmethod
    def paginated(data, page, per_page, total, total_pages):
        """Create paginated response"""
        return APIResponse.success(
            data=data,
            meta={
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                }
            }
        )
