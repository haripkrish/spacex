import logging


class LoggerConfig:
    def __init__(self):
        # Create a logger
        self.logger = logging.getLogger("spacex")
        self.logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


logger = LoggerConfig().get_logger()
