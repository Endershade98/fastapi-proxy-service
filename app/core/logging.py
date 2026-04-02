import logging

class LoggerConfig:
    """Logger configuration class."""

    @staticmethod
    def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """Set up a logger instance with the specified name and level."""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger
    
    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """Get a logger instance with the specified name and level."""
        return LoggerConfig.setup_logger(name, level)