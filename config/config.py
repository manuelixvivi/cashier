"""
Application Configuration
Centralized configuration using environment variables
"""

import os
from datetime import timedelta


class Config:
    """Base Configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/pos_ai_db')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'pos_ai_db')

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_HOURS', '24')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', '30')))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ERROR_MESSAGE_KEY = 'message'

    # Redis & Celery
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Jakarta'
    CELERY_ENABLE_UTC = True

    # AI Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    GEMMA_MODEL = os.getenv('GEMMA_MODEL', 'gemma-7b-it')
    AI_MODE = os.getenv('AI_MODE', 'offline')

    # Business Settings
    STORE_NAME = os.getenv('STORE_NAME', 'Toko Saya')
    STORE_ADDRESS = os.getenv('STORE_ADDRESS', '')
    STORE_PHONE = os.getenv('STORE_PHONE', '')
    CURRENCY = os.getenv('CURRENCY', 'IDR')
    TAX_RATE = float(os.getenv('TAX_RATE', '0.0'))

    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', '20'))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', '100'))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')

    # Forecasting
    FORECAST_DAYS = int(os.getenv('FORECAST_DAYS', '30'))
    FORECAST_CONFIDENCE_INTERVAL = float(os.getenv('FORECAST_CONFIDENCE_INTERVAL', '0.95'))


class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/pos_ai_dev')


class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """Testing Configuration"""
    TESTING = True
    MONGO_URI = os.getenv('MONGO_TEST_URI', 'mongodb://localhost:27017/pos_ai_test')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    WTF_CSRF_ENABLED = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
