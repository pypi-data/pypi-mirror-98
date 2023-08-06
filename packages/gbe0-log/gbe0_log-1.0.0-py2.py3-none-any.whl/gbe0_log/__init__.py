# -*- coding: utf-8 -*-

"""
My standard logging module
"""

# Import logging and set null handler
import logging

# Set default logging handler to avoid "No handler found" warnings
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

# Import version info
from .__version__ import __version__

# Import main module
from .logger import Logger