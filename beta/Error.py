# -*- coding: utf-8 -*-
"""
This file contain all the error classes
"""

class MtubeError(Exception):
	pass

class ParsecError(Exception):
	pass

class RegexError(Exception):
	pass

class VideoInfo(Exception):
	pass

class InvalidVideoUrl(Exception):
	pass

class GeoBlockingError(Exception):
	pass

class FFMPEG_Not_Found(Exception):
	pass

class ResolutionError(Exception):
	pass