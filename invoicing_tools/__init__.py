"""Top-level package for Invoicing Tools."""


__author__ = """Luis Carlos Berrocal"""
__email__ = 'luis.berrocal.1942@gmail.com'
__version__ = '0.3.2'

from invoicing_tools.config.configuration import ConfigurationManager

CONFIGURATION_MANAGER = ConfigurationManager()


def logger_configuration():
    import logging.config
    from invoicing_tools.settings import LOGGING
    logging.config.dictConfig(LOGGING)
    import logging

    logger = logging.getLogger(__name__)
    logger.debug('Configured logger.')


logger_configuration()
