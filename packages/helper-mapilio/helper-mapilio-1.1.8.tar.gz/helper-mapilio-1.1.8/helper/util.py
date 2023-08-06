import logging
from decimal import Decimal

NUMBER_TYPES = (int, float, Decimal)

__version__ = "1.1.7"

logger = logging.getLogger('helper')


def get_version():
    return __version__
