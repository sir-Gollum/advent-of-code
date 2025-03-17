# coding: utf-8
import logging
import logging.config

DEBUG = "DEBUG"
INFO = "INFO"


def configure_logging(level, format="%(message)s"):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": format,
                },
            },
            "handlers": {
                "default": {
                    "level": level,
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": level,
                },
            },
        }
    )


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
