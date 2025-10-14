import logging

def create_logger(name):
    """Create logger and set config for consistency across modules"""
    logger = logging.getLogger(name)

    FORMAT = '[{levelname} - {name} - {asctime}] {message}'
    logging.basicConfig(format=FORMAT, style='{', level=logging.INFO)

    return logger
