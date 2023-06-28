import logging

from pythonjsonlogger import jsonlogger


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(pathname)s:%(lineno)s %(message)s',
        json_ensure_ascii=False
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
