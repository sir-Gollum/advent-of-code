# coding: utf-8
import logging
import logging.config

DEBUG = 'DEBUG'
INFO = 'INFO'


def configure_logging(level, format="%(message)s"):
    logging.config.dictConfig({
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
        }
    })
