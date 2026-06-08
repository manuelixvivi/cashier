"""
Application Constants
"""

from enum import Enum


class UserRole(Enum):
    """User roles"""
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    MANAGER = 'manager'
    CASHIER = 'cashier'
    INVENTORY_STAFF = 'inventory_staff'


class TransactionStatus(Enum):
    """Transaction statuses"""
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'


class PaymentMethod(Enum):
    """Payment methods"""
    CASH = 'cash'
    DEBIT = 'debit'
    CREDIT = 'credit'
    QRIS = 'qris'
    EWALLET = 'ewallet'


class InventoryMovementType(Enum):
    """Inventory movement types"""
    GOODS_RECEIPT = 'goods_receipt'
    STOCK_OUT = 'stock_out'
    STOCK_ADJUSTMENT = 'stock_adjustment'
    STOCK_TRANSFER = 'stock_transfer'
    SALE = 'sale'
    PURCHASE_RETURN = 'purchase_return'


class UnitType(Enum):
    """Product unit types"""
    PIECE = 'pcs'
    BOX = 'box'
    PACK = 'pack'
    STRIP = 'strip'
    BOTTLE = 'bottle'
    CARTON = 'carton'
    DOZEN = 'dozen'
    GRAM = 'gram'
    KILOGRAM = 'kg'
    METER = 'meter'
    LITER = 'liter'


class ReportPeriod(Enum):
    """Report periods"""
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


class AIMode(Enum):
    """AI Chatbot modes"""
    ONLINE = 'online'
    OFFLINE = 'offline'
    HYBRID = 'hybrid'


# Permission constants
PERMISSIONS = {
    'user': ['create', 'read', 'update', 'delete'],
    'product': ['create', 'read', 'update', 'delete', 'import', 'export'],
    'inventory': ['view', 'adjust', 'transfer', 'opname'],
    'sale': ['create', 'read', 'cancel', 'refund', 'discount'],
    'purchase': ['create', 'read', 'approve', 'cancel'],
    'report': ['view_daily', 'view_weekly', 'view_monthly', 'view_yearly', 'export'],
    'analytics': ['view_dashboard', 'view_sales', 'view_inventory', 'view_customer'],
    'forecasting': ['view', 'run'],
    'settings': ['view', 'update'],
    'chatbot': ['use', 'configure'],
    'audit': ['view']
}
