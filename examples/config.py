import logging
import sys

from pypvserver import PypvServer

server_prefix = 'PYPVSERVER:'

LOG_FORMAT = "%(asctime)-15s [%(name)5s:%(levelname)s] %(message)s"
logger = logging.getLogger(__name__)
_server = None


def setup_logging(loggers, level=logging.DEBUG):
    '''Set up debug loggers for the examples'''

    for name in loggers:
        logger = logging.getLogger(name)
        log_fmt = logging.Formatter(LOG_FORMAT)
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(log_fmt)

        logger.setLevel(level)
        logger.addHandler(log_handler)


def get_server():
    global _server

    if _server is not None:
        return _server

    # enable logging for this module
    setup_logging([__name__])

    logger.info('Creating channel access server with prefix: %s',
                server_prefix)

    _server = PypvServer(prefix=server_prefix)
    return _server
