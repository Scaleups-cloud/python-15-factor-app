import logging
from pythonjsonlogger import jsonlogger

def setup_logger(name):
    """
    Sets up a structured JSON logger.
    """
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(jsonlogger.JsonFormatter())

    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

    return logger