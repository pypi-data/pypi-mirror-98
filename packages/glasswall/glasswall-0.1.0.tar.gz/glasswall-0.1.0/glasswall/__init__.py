

__version__ = "0.10.0"

import ctypes
import logging
import os
import platform
import tempfile
from datetime import datetime

_PYTHON_VERSION = platform.python_version()
_OPERATING_SYSTEM = platform.system()
_ROOT = os.path.dirname(__file__)
_TEMPDIR = os.path.join(tempfile.gettempdir(), "glasswall")

from glasswall import config, content_management, determine_file_type, utils
from glasswall.libraries.archive_manager.archive_manager import ArchiveManager
from glasswall.libraries.editor.editor import Editor
from glasswall.libraries.rebuild.rebuild import Rebuild
from glasswall.libraries.security_tagging.security_tagging import SecurityTagging
from glasswall.libraries.word_search.word_search import WordSearch


class GwReturnObj:
    """ A Glasswall return object. """

    def __init__(self, **kwargs):
        [setattr(self, k, v) for k, v in kwargs.items()]
