import logging


def setup_logging() -> None:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(pathname)s:%(lineno)-4s %(message)s',
        level=logging.INFO,
        datefmt='%d-%m-%Y %H:%M:%S'
    )
