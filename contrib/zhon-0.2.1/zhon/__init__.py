"""Provides constants used in Chinese text processing."""

__version__ = '0.2.1'

import logging

from . import str
from . import cedict
from . import pinyin

logger = logging.getLogger(__name__)
try:
    logger.addHandler(logging.NullHandler())
except AttributeError:  # catch error for Python 2.6
    pass
