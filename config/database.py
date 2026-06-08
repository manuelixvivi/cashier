"""
Database Connection Manager
Singleton pattern for MongoDB connection management
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from flask import current_app, g
import logging

logger = logging.getLogger(__name__)


class Database:
    """
    Database Manager using Singleton Pattern
    Handles MongoDB connection lifecycle
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, app=None):
        """Initialize database connection"""
        if app is None:
            app = current_app

        mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/pos_ai_db')
        db_name = app.config.get('MONGO_DB_NAME', 'pos_ai_db')

        try:
            cls._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            cls._client.admin.command('ping')
            cls._db = cls._client[db_name]
            logger.info(f"Connected to MongoDB: {db_name}")

            cls._create_indexes()
            return cls._db

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    @classmethod
    def _create_indexes(cls):
        """Create database indexes for performance"""
        if cls._db is None:
            return

        cls._db.users.create_index('username', unique=True)
        cls._db.users.create_index('email', unique=True)
        cls._db.products.create_index('sku', unique=True)
        cls._db.products.create_index('barcode', unique=True, sparse=True)
        cls._db.products.create_index('name')
        cls._db.products.create_index('category')
        cls._db.transactions.create_index('transaction_code', unique=True)
        cls._db.transactions.create_index('created_at')
        cls._db.transactions.create_index('cashier_id')
        cls._db.inventory.create_index('product_id')
        cls._db.inventory.create_index('warehouse_location')
        cls._db.audit_logs.create_index('timestamp')
        cls._db.audit_logs.create_index('user_id')
        cls._db.audit_logs.create_index('action')
        cls._db.chatbot_logs.create_index('timestamp')
        cls._db.chatbot_logs.create_index('session_id')

        logger.info("Database indexes created successfully")

    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls._db is None:
            cls.initialize()
        return cls._db

    @classmethod
    def get_client(cls):
        """Get MongoDB client instance"""
        return cls._client

    @classmethod
    def close(cls):
        """Close database connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")

    @classmethod
    def health_check(cls):
        """Check database health"""
        try:
            if cls._client:
                cls._client.admin.command('ping')
                return True
            return False
        except Exception:
            return False


def get_db():
    """Helper function to get database instance"""
    return Database.get_db()
