import logging
import os
import sys
from pythonjsonlogger import jsonlogger


def configure_logging(level: str = None):
    level = level or os.getenv('LOG_LEVEL', 'INFO')
    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    # remove existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers = []

    logger.addHandler(handler)


def get_logger(name: str):
    configure_logging()
    return logging.getLogger(name)
