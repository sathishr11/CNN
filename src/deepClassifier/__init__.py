import os
import sys
import logging
import threading
from datetime import datetime


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Logger(Singleton):
    def __init__(self) -> None:
        # create filename for logging
        log_file_name = f'log_{datetime.now().strftime("%Y_%m_%d")}.log'

        # create the path for log files
        log_file_path = os.path.join("logs", log_file_name)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        # Create a custom logger
        logging.basicConfig(level=logging.NOTSET)
        self.logger = logging.getLogger(__name__)

        # Create handlers
        terminal_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler(log_file_path)
        terminal_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.NOTSET)

        # Create formatters and add it to handlers
        terminal_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_format = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
        )
        terminal_handler.setFormatter(terminal_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        self.logger.addHandler(terminal_handler)
        self.logger.addHandler(file_handler)


logger = Logger().logger
