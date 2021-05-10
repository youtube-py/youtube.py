# -*- coding: utf-8 -*-
"""
Here we have main classes

"""
from typing import Union, Callable
from typing import List
from typing import Dict
from typing import Any
import requests, json
import logging, sys
from .Stream import Stream
from .Stream import Queue
from time import ctime
from .Connection import HTTP
import concurrent.futures
from .Add_ons import (
	Get_vid_info_url,
	Get_r_vid_info_url,
	Get_video_id,
	Decipher_signature,
	Get_playlist_id,
	Extract_from_web_json
	)
from .Extract import (
	Is_age_restricted,
	Get_js,
	Get_video_info,
	Req_get,
	Get_playlist_videos,
	Continuation,
	Search_results
	)


logg = logging.getLogger(__name__)


HIGH = 0
MID = 1
LOW = 2


class Obj():
	def __init__(self,code:str, proxy:str="",id:int=1, name:str="") -> None:
		self.code = code
		self.proxy = proxy
		self.id = id
		self.name = name
		if not id:
			self.id = id
		if not name:
			self.name = "None"
		if not proxy:
			self.proxy = "None"

			
	def __str__(self) -> str:
		return f"<Class {self.__class__.__name__} VID={self.code} PROXY={self.proxy} ID={self.id} NAME={self.name} {hex(id(self))}>"
	def __repr__(self) -> str:
		return f"<Class {self.__class__.__name__} VID={self.code} PROXY={self.proxy} ID={self.id} NAME={self.name} {hex(id(self))}>"

class Video(Obj):
	'''
	Construct a :class:`Video <Video>` object.

	:param str url: Pass youtube valid video url. 
		ie. https://www.youtube.com/watch?v=9NQqaKz7eyI
	:param str proxy: (optional) pass the proxy url
		example: 
			``socks5://admin:admin@127.0.0.1:9050``,
			``http://admin:admin@127.0.0.1:8000``,
			``https://127.0.0.1:8000``

	:param int id: (optional) Video class id just to identify easily.
	:param object id: (optional) Pass the HTTP object.
	:param int name: (optional) if you want specify name.

	:rtype: None
	:returns: None
	'''
	def __init__(self,url:str, proxy:str="", id:int=1, http:HTTP=None, name:str="") -> None:
		self.http = http
		if not http:
			self.http = HTTP.MakeObject(proxy=proxy)
		self.video_id=Get_video_id(url)
		super().__init__(self.video_id,proxy,id, name)
		logg.debug(f"Working on Video id <{self.video_id}>")
		self.video_watch_url:str=f"https://www.youtube.com/watch?v={self.video_id}"

		self.js_url, self.video_html=Get_js(self.http,self.video_id)

		#Videos containers 
		self.fmts:Dict[Any,Any] = {}
		self.age_restricted:bool = False

		#Raw data store
		self.js:str=""
		self.video_info_url:str=""
		self.video_info:Dict[Any, Any]={}
		self.issig:bool=False

		self.Prefetch()


	def Prefetch(self) -> None:
		'''
		This will extract and do most of the work

		'''
		self.age_restricted = Is_age_restricted(self.video_html)
		if self.age_restricted:
			self.video_info_url = Get_r_vid_info_url(self.video_id)
		else:
			self.video_info_url = Get_vid_info_url(self.video_id,self.video_watch_url)

		self.fmts , self.issig, self.video_info =  Get_video_info(self.http,self.video_info_url)
		self.js=Req_get(self.http,self.js_url)

		if self.issig:
			Decipher_signature(self.fmts,self.js)

	@property
	def get_dict(self):
		'''
		This will return the raw dict of video streams urls
		'''
		return self.fmts
	

	@property
	def streams(self) -> Queue:
		'''
		Will returns :class:`Queue <Queue>`
				
		:rtype: :class:`Queue <Queue>`
		:returns: Returns the Queue object
		'''
		tmp = sorted(self.fmts,key= lambda x: x["itag"])
		return Queue([Stream(n, self.title) for n in self.fmts])

	@property
	def videoId(self) -> str:
		'''
		This will return the video id.

		:rtype: str
		:returns: str
		'''
		return self.video_info['videoDetails']['videoId']

	@property
	def title(self) -> str:
		'''
		This will return the video title.

		:rtype: str
		:returns: str
		'''
		return self.video_info['videoDetails']['title'].replace("+"," ")


	@property
	def length(self) -> int:
		'''
		This will return the video time in second.

		:rtype: int
		:returns: int
		'''
		return int(self.video_info['videoDetails']['lengthSeconds'])

	@property
	def keywords(self) -> List[str]:
		'''
		This will return the video keywords.

		:rtype: List[str]
		:returns: List[str]
		'''
		return self.video_info['videoDetails']['keywords']

	@property
	def channel(self) -> str:
		'''
		This will return the video channel id.

		:rtype: str
		:returns: str
		'''
		return self.video_info['videoDetails']['channelId']

	@property
	def description(self) -> str:
		'''
		This will return the video description.

		:rtype: str
		:returns: str
		'''
		return self.video_info['videoDetails']['shortDescription'].replace("+", " ")


	@property
	def author(self) -> str:
		'''
		This will return the video author.

		:rtype: str
		:returns: str
		'''
		return self.video_info['videoDetails']['author'].replace("+", " ")

	@property
	def views(self) -> int:
		'''
		This will return the total video views.

		:rtype: int
		:returns: int
		'''
		return int(self.video_info['videoDetails']['viewCount'])

	@property
	def thumbnail(self) -> str:
		'''
		This will return the video thumbnail.

		:rtype: str
		:returns: str
		'''
		return self.video_info['videoDetails']['thumbnail']['thumbnails'][-1]['url']




class PlayList:
	'''
	Construct a :class:`PlayList <PlayList>`

	:param str url: Pass youtube valid playlist url. 
		ie. https://www.youtube.com/watch?v=9NQqaKz7eyI
	:param str proxy: (optional) pass the proxy url
		example: 
			``socks5://admin:admin@127.0.0.1:9050``
			``http://admin:admin@127.0.0.1:8000``
			``https://127.0.0.1:8080``
	:param bool process: (optional) Process will trigger the function for making objects of
			 :class:`Video <Video>` with the list of playlist videos default (False), When (True)
			 it will take some extra time depend on your CPU and Internet speed. Process will use 10 workers 
			 to create objects fasts.
	'''
	def __init__(self,url:str, proxy:str="", process:bool=False) -> None:
		self.http = HTTP.MakeObject(proxy=proxy)
		if proxy:
			logg.debug(f'Starting with proxy: {proxy}')


		# Holds playlist id `list=`
		self.playlist_id = Get_playlist_id(url)
		
		self.playlist_url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

		self.html_parsec_json = Get_playlist_videos(self.http,self.playlist_url)

		# Holds the objects of class Video
		self.obj_videos = []
		self.get_videos()
		if process:
			self.processing()
	
	@property
	def get_dict(self):
		'''
		This will return the list of :class:`Video <Video>` if available or will just return the dict of vid and name, 
		Availability of :class:`Video <Video>` objects is depend on your ``PlayList(url,process=False)``, process will process
		all videos to :class:`Video <Video>` objects.
		'''
		if self.obj_videos:
			return self.obj_videos
		return self.videos

	@property
	def get_object(self):
		'''
		This will return the list of :class:`Video <Video>` objects, even when you ``process=False``.
		'''
		if not self.obj_videos:
			self.processing()
		return self.obj_videos
	

	def processing(self):
		'''
		Processing will process all videos to :class:`Video <Video>` object
		'''
		func = lambda x,y: Video(url=f'https://youtu.be/{x["vid"]}',http=self.http,name=f'{x["name"]}',id=y)
		with  concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
			for n in executor.map(func,self.videos,range(len(self.videos))):
				logg.debug(f'CLASS playlist created video object {n}')
				self.obj_videos.append(n)
		logg.debug(f'All objects of :class:`Video` created')

	def get_videos(self):
		'''
		Here we will process all videos dict
		'''
		self.videos, token = Extract_from_web_json(self.html_parsec_json)
		while token:
			token = Continuation(self.http, self.videos, token)

		logg.debug(f'Playlist collected {len(self.videos)}')

	def downloadall(self,quality:int) -> None:
		'''
		This is to download all playlist videos, remember this will download all videos
		synchronizly. Thiw function will download one file (audio/video) you may not satisfied with the quality. 

		+---------+---------+
		| Quality | Value   |
		+=========+=========+
		| HIGH    |   0     |
		+---------+---------+
		| MID     |   1     |
		+---------+---------+
		| LOW     |  2 or n |
		+---------+---------+

		:param int quality: Pass the quality type
		'''
		if not self.obj_videos:self.processing()
		logg.debug(f'Download all with quality type {quality}')
		if not self.obj_videos:
			self.processing()
		if quality == 0:
			for n in self.obj_videos:
				print(f'Downloading {n.title}')
				n.streams.get_both.high().download()
		elif quality == 1:
			for n in self.obj_videos:
				print(f'Downloading {n.title}')
				n.streams.get_both.mid().download()
		else:
			for n in self.obj_videos:
				print(f'Downloading {n.title}')
				n.streams.get_both.low().download()


class Search:
	'''
	This will search your query on youtube and will return videos.

	:param str query:
		Pass the query for search.
	:param str country: (optional)
		Pass the ISO 2 country code.
	:param str proxy: (optional) pass the proxy url
		example: 
			``socks5://admin:admin@127.0.0.1:9050``
			``http://admin:admin@127.0.0.1:8000``
			``https://127.0.0.1:8080``
	:param bool process: (optional) Process will trigger the function for making objects of
		 :class:`Video <Video>` with the list of playlist videos default (False), When (True)
		 it will take some extra time depend on your CPU and Internet speed. Process will use 10 workers 
		 to create objects fasts.
	
	:rtype: None
	:returns: None

	'''

	def __init__(self,query:str, country:str="", proxy:str="", process:bool=False) -> None:
		self.http = HTTP.MakeObject(proxy=proxy)

		if proxy:
			logg.debug(f'Starting with proxy: {proxy}')
		self.query = query
		self.country = country
		self.videos = []
		self.obj_videos = []
		self.search_start()
		if process:
			self.processing()
	@property
	def get_dict(self):
		'''
		This will return the list of :class:`Video <Video>` if available or will just return the dict of vid and name, 
		Availability of :class:`Video <Video>` objects is depend on your ``Search(query,process=False)``, process will process
		all videos to :class:`Video <Video>` objects.
		'''
		if self.obj_videos:
			return self.obj_videos
		return self.videos

	@property
	def first(self):
		'''
		Will return the first search video.

		:rtype: :class:`Video <Video>`
		:returns: This will return :class:`Video <Video>` of first search video.
		'''
		if self.obj_videos:
			return self.obj_videos[0]
		return Video(url=f'https://youtu.be/{self.videos[0]["vid"]}',http=self.http,name=f'{self.videos[0]["name"]}')

	@property
	def get_object(self):
		'''
		This will return the list of :class:`Video <Video>` objects, even when you ``process=False``.
		'''
		if not self.obj_videos:
			self.processing()
		return self.obj_videos

	def processing(self):
		'''
		Processing will process all videos to :class:`Video <Video>` object
		'''
		func = lambda x,y: Video(url=f'https://youtu.be/{x["vid"]}',http=self.http,name=f'{x["name"]}',id=y)
		with  concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
			for n in executor.map(func,self.videos,range(len(self.videos))):
				logg.debug(f'CLASS playlist created video object {n}')
				self.obj_videos.append(n)
		logg.debug(f'All objects of :class:`Video` created')

	def search_start(self):
		status = Search_results(self.http, self.query, self.videos, self.country)
		if status:
			logg.debug(f'Search completed and found {len(self.videos)} videos')

	def __iter__(self):
		if self.obj_videos:
			return iter(self.obj_videos)
		return iter(self.videos)

	def __repr__(self):
		return f"{self.videos}"

	def __getitem__(self, i: Union[int, slice]) -> Union[Stream, List[Stream]]:
		if self.obj_videos:
			return self.obj_videos[i]
		return self.videos[i]