import logging
import os


class Filter(logging.Filter):
    def __init__(self, name):
        self.name = name
    def filter(self, record):
        record.app_name = self.name
        return True

def create_logger(dt_str, logger_name, short_name):
    # Initital Logger Setup
    logger = logging.getLogger(f"{logger_name}")
    logger.addFilter(Filter(logger_name))
    logger.setLevel(logging.DEBUG)

    # File Logging
    file_log_handler = logging.FileHandler(f"../logs/stock_bot_{short_name}_{dt_str}.log")
    file_log_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s [%(app_name)4s] %(message)s"))
    file_log_handler.setLevel(logging.DEBUG)

    # Stream Logging to StdOut
    LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s [%(app_name)4s] %(message)s"))
    stream_handler.setLevel(LOGLEVEL)

    # Combine Stream and File Logging into same Logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_log_handler)
    return logger
