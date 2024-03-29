from pathlib import Path

from invoicing_tools import CONFIGURATION_MANAGER

try:
    CONFIGURATION = CONFIGURATION_MANAGER.get_configuration()
    LOG_FOLDER = CONFIGURATION['logs']['folder']
    LOG_FILE = Path(f'{LOG_FOLDER}/{CONFIGURATION["logs"]["filename"]}')
except KeyError:
    error_message = 'Error getting logs configuration. Check the configuration file.'
    LOG_FILE = CONFIGURATION_MANAGER.logs_folder / f'{CONFIGURATION_MANAGER.APP_NAME}.log'
    print(error_message)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(lineno)d  "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": str(LOG_FILE),
            "maxBytes": 1024 * 1024,
            "backupCount": 3
        }
    },
    "loggers": {
        'invoicing_tools': {
            "level": "DEBUG",
            "handlers": ['console', 'file'],
            "propagate": False
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", 'file']},
}
