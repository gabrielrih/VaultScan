import logging
import logging.config


class Logger:
    @staticmethod
    def get_logger(name, verbose: bool = False):
        log_level = 'INFO'
        if verbose:
            log_level = 'DEBUG'
        logger = logging.getLogger(name)
        logger.setLevel(level=log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(levelname)s [%(filename)s:%(lineno)d] - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
