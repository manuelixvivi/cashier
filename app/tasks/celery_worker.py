"""
Celery Worker Configuration
"""

from app import make_celery

celery = make_celery()
