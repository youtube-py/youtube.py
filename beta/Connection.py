# -*- coding: utf-8 -*-
"""
Here we have HTTP class for sending all requests
"""
from typing import Union, Callable
from typing import List, Tuple
from typing import Dict, Type
from typing import Any, Optional
from requests import get
from requests import Response
from urllib.parse import urlparse


class HTTP:
	'''
	This class from where we will make all requests

	example:
		HTTP.MakeObject() and this will return a requests class object without proxy

		:param Optional[str] proxy:
			(optional) Pass the proxy url
      
			example: 
				``socks5://admin:admin@127.0.0.1:9050``,
				``http://admin:admin@127.0.0.1:8000``,
				``https://127.0.0.1:8000``

	'''
	def __init__(self,*args:Tuple[str],**kwargs: Dict[str,Any]) -> None:
		self.args = args
		self.kwargs = kwargs

	def _GET(self, url:str, **kwargs: Dict[str,Any]) -> Response:
		self.kwargs.update(kwargs)
		return get((url), **self.kwargs)

	@classmethod
	def MakeObject(cls, proxy:Optional[str]=None) -> "HTTP":
		if proxy:
			u = urlparse(proxy)
			proxies = dict(
				http = f"{u.scheme}://{u.netloc}",
				https = f"{u.scheme}://{u.netloc}")
			return cls(proxies=proxies)
		return cls()
