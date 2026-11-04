import logging
import sys


def configure_logging(log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("pipeline")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = configure_logging()
