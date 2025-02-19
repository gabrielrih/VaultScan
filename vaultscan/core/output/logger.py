import logging
import logging.config

from vaultscan.core.configs import AvailableConfigs, ConfigManager


IS_VERBOSE = ConfigManager(AvailableConfigs.VERBOSE).get_value()
LOG_LEVEL = 'DEBUG' if IS_VERBOSE else 'INFO'


class LoggerFactory:
    @staticmethod
    def get_logger(name):
        return Logger.get_logger(name)


class LogColors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": LogColors.BLUE,
        "INFO": LogColors.RESET,
        "SUCCESS": LogColors.GREEN,
        "WARNING": LogColors.YELLOW,
        "ERROR": LogColors.RED,
        "CRITICAL": LogColors.RED,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, LogColors.RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{LogColors.RESET}"


# Define a new log level for success messages
SUCCESS_LEVEL = 25  # Between INFO (20) and WARNING (30)
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
    """Custom log method for success messages."""
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

# Add the method dynamically to logging.Logger
logging.Logger.success = success


class Logger:
    @staticmethod
    def get_logger(name):
        logging.addLevelName(25, 'SUCCESS')  # Between INFO 20 and WARNING 30
        logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL)

        handler = logging.StreamHandler()
        handler.setLevel(LOG_LEVEL)

        # Define different formats
        # When running in debug mode, add more information on the logs
        format = "%(levelname)s: %(message)s"
        if LOG_LEVEL == 'DEBUG':
            format = "%(levelname)s - %(message)s [%(name)s] [%(filename)s:%(lineno)d]"
        
        # Apply debug format only for DEBUG level
        formatter = ColoredFormatter(format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
