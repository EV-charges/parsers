import logging

import logstash
from pythonjsonlogger import jsonlogger


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(pathname)s:%(lineno)s %(message)s',
        json_ensure_ascii=False
    )
    logstah_handler = logstash.TCPLogstashHandler(host='localhost', port=50000, version=1)
    log_handler.setFormatter(formatter)

    logger.addHandler(logstah_handler)
    logger.addHandler(log_handler)
