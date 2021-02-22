import logging
import os

def create_logger(dt_str):
    # Initital Logger Setup
    logger = logging.getLogger("stock_bot")
    logger.setLevel(logging.DEBUG)

    # File Logging
    file_log_handler = logging.FileHandler(f"../logs/stock_bot_{dt_str}.log")
    file_log_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s [%(levelname)4s] %(message)s"))
    file_log_handler.setLevel(logging.DEBUG)

    # Stream Logging to StdOut
    LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s [%(levelname)4s] %(message)s"))
    stream_handler.setLevel(LOGLEVEL)

    # Combine Stream and File Logging into same Logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_log_handler)
    return logger
