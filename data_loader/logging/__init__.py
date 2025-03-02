import logging


def setup_logger(namespace, log_filename, log_level=logging.INFO):
    """
    Setup a single logging stream.
    """

    handler = logging.FileHandler(log_filename)
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        )
    
    logger = logging.getLogger(namespace)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger
