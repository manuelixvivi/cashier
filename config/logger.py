"""
Structured Logging Configuration
"""

import logging
import sys
import structlog


def configure_logging(log_level='INFO', log_format='json'):
    """Configure structured logging for the application"""
    logging.basicConfig(
        format='%(message)s',
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if log_format == 'json' 
            else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def get_logger(name=None):
    """Get structured logger instance"""
    return structlog.get_logger(name)
