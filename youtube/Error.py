# -*- coding: utf-8 -*-
"""
This file contain all the error classes
"""

class YoutubeError(Exception):
	def __init__(self, msg):
		self.msg = msg
		Exception.__init__(self, msg)

	def __str__(self):
		return self.msg

	__repr__ = __str__


class ParsecError(YoutubeError):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg

class RegexError(Exception):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg

class VideoInfo(Exception):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg

class InvalidVideoUrl(Exception):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg

class GeoBlockingError(Exception):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg

class FFMPEG_Not_Found(Exception):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg
class ResolutionError(Exception):
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return self.msg

class GoogleReCaptchaError(Exception):
	def __init__(self):
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return "IP blacklisted or you might using proxy."