"""
Utility Helpers
"""

from datetime import datetime


def format_currency(amount, currency='IDR'):
    """Format amount as currency"""
    if currency == 'IDR':
        return f"Rp {amount:,.0f}"
    return f"{amount:,.2f}"


def parse_date(date_str, format='%Y-%m-%d'):
    """Parse date string"""
    if not date_str:
        return None
    return datetime.strptime(date_str, format)


def generate_code(prefix, length=6):
    """Generate unique code"""
    from bson import ObjectId
    return f"{prefix}-{datetime.utcnow().strftime('%Y%m%d')}-{str(ObjectId())[-length:]}"


def sanitize_string(text):
    """Sanitize string input"""
    if not text:
        return ''
    return text.strip()


def paginate_results(items, page, per_page):
    """Paginate list of items"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        'items': items[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': (total + per_page - 1) // per_page
    }
