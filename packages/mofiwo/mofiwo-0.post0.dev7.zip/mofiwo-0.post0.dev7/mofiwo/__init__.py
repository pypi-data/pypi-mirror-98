"""init.py module"""
import logging

from mofiwo.logger import FORMATTER_INFO, FORMATTER_DEBUG

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(FORMATTER_INFO))

log.addHandler(stream_handler)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
