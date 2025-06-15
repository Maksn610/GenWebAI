import logging

logger = logging.getLogger("genwebai")
logger.setLevel(logging.INFO)
logger.propagate = False

formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
