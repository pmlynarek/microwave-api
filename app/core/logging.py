import logging


def get_logger(name=None):
    name = name or __name__
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
