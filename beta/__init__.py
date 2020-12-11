# -*- coding: utf-8 -*-
"""
Youtube.py is really lite python liberary with ultra fast downloader
"""

from .Config import (__title__,__version__,__issues__,
	__author__,__license__, __copyright__, __github__)
from .__main__ import Video, PlayList, HIGH, LOW, MID, Search
from .Connection import HTTP
from .Stream import Stream
from .Stream import Queue
from .Stream import FFMPEG
from .Cipher import Cipher
from .Error import *
from .Downloader import Download
import logging, sys 


# logging.basicConfig(level=logging.DEBUG, filename="mtube.log", filemode="w",
# 	format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s")


