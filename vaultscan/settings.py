import os

from enum import Enum
from dotenv import load_dotenv
load_dotenv() # loading .env file


class LogLevel(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


class GlobalSettings:
    @property
    def log_level(self) -> LogLevel:
        log_level = os.getenv("LOG_LEVEL", "INFO")
        return LogLevel(log_level.lower())
