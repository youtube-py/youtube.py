# -*- coding: utf-8 -*-
"""
Here we have 2 classes where we will
manage/sort the streams and return the 
download object
"""

from typing import Union, Callable
from typing import List, NoReturn
from typing import Dict, Optional
from typing import Any, Tuple
from subprocess import run
from .Error import (FFMPEG_Not_Found, ResolutionError)
from .Downloader import Download
from .Config import __docs__
import logging, time, os

logg = logging.getLogger(__name__)

class Stream:
	'''
	Here we will process :class:`Stream <Stream>`

	:param Dict[Any,Any] stream: singal dict of stream json
	:param str name: Pass the video title

	'''

	def __init__(self,stream:Dict[Any, Any], name:str) -> None:
		
		self.stream = stream
		self.name = name

		rep = f'<Class {self.__class__.__name__}: '
		if stream["type"] != "audio":
			rep += f'itag="{self.stream["itag"]}" '
			rep += f'qualityLabel="{self.stream["qualityLabel"]}" '
			rep += f'fps="{self.stream["fps"]}" '
			rep += f'mime="{self.stream["mimeType"]}" '
			rep += f'type="{self.stream["type"]}" '
			rep += f'format="{self.stream["format"]}" '
			rep += f'codecs="{self.stream["codecs"]}"'
			rep += f'>'
		else:
			rep += f'itag="{self.stream["itag"]}" '
			rep += f'bitrate="{self.stream["bitrate"]}" '
			rep += f'mime="{self.stream["mimeType"]}" '
			rep += f'type="{self.stream["type"]}" '
			rep += f'format="{self.stream["format"]}" '
			rep += f'codecs="{self.stream["codecs"]}"'
			rep += f'>'
		self.rep = rep

	def __str__(self) -> str:
		return self.rep

	def __repr__(self) -> str:
		return self.rep
	
	def check(self,a:str) -> str:
		'''
		Here we will take a and return the values,
		``a`` could be  ``qualityLabel`` or ``type``
		qualityLabel: will return ``resolution of the video``
		type: will return ``video, audio or both``
		'''
		if a == "qualityLabel":
			if self.stream["type"] != "audio":
				return int(self.stream[a].replace("p",""))
			else:
				return self.stream["bitrate"]
		if a == "type":
			return self.stream["type"]

	@property
	def is_audio(self) -> bool:
		'''
		Check is the stream is audio

		:rtype: bool
		:returns: check the stream and return bool(true, false)
		'''
		if self.stream["type"] == "audio":
			return True
		return False
	
	@property
	def is_video(self) -> bool:
		'''
		Check is the stream is video

		:rtype: bool
		:returns: check the stream and return bool(true, false)
		'''
		if self.stream["type"] == "video":
			return True
		return False

	@property
	def is_both(self) -> bool:
		'''
		Check is the stream has audio/video

		:rtype: bool
		:returns: check the stream and return bool(true, false)
		'''
		if self.stream["type"] == "both":
			return True
		return False
	
	@property
	def url(self) -> str:
		'''
		This will return the URL of thie Stream

		:rtype: str
		:returns: url of video in str
		'''
		return self.stream["url"]

	@property
	def format(self) -> str:
		'''
		This will return the stream format

		:rtype: str
		:returns: format of video in str
		'''
		return self.stream["format"]
	
	@property
	def itag(self) -> int:
		'''
		This will return the stream format

		:rtype: int
		:returns: itag of video in int
		'''
		return self.stream["itag"]
	
	def download(self, dire:str="", name:str="",status:bool=False,connection:int=8, chunk:int=5120, unique:bool=False) -> Download:
		'''
		This will return the :class:`Download <Download>`
		
		:param str name: 
			(optional) Pass the name of file name. 
		:param str dire: 
			(optional) Pass the dir for output file with excluding filename.
		:param bool status: 
			(optional) Pass if you want to enable process bar. ``Default[False]``
		:param int connection: 
			(optional) Pass number is connection to be create. ``Default[8]``
		:param int chunk: 
			(optional) Pass the chunk/buffer size for accepting packets. ``Default[5120]``
		:param int unique:
			(optional) Pass if you want unique prefix, **Default[False]**

		:rtype: :class:`Download <Download>`
		:returns: :class:`Download <Download>` object
		'''
		fname = self.filename
		if name:
			fname=name
		return Download(url=self.url, dire=dire, name=fname , status=status, connection=connection, chunk=chunk, unique=unique).start()


	@property
	def filename(self) -> str:
		'''
		This will generate file name (this function is for internal use)

		:rtype: : str
		:returns: filename in str
		'''
		return f'{self.name}.{self.stream["format"]}'


class FFMPEG:
	'''
	Here we will download 2 stream audio/video, 
	and copy them in one file with ffmpeg

	:param List[Stream] av:
		pass the stream of audio and video in list,

	:rtype: None
	:returns: Nothing will get return
	'''
	def __init__(self,av:List[Stream]) -> None:
		if not self.check_ffmpeg():
			pass
		self.av = av
	def __repr__(self):
		return f"{self.av}"
	def download(self,dire:str="", name:str="",status:bool=False,connection:int=8, chunk:int=5120, unique:bool=False) -> str:
		'''
		This will return bool value as video download convert status`
		
		:param str name: 
			(optional) Pass the name of file name. 
		:param str dire: 
			(optional) Pass the dir for output file with excluding filename.
		:param bool status: 
			(optional) Pass if you want to enable process bar. **Default[False]**
		:param int connection: 
			(optional) Pass number is connection to be create. **Default[8]**
		:param int chunk: 
			(optional) Pass the chunk/buffer size for accepting packets. **Default[5120]**
		:param int unique:
			(optional) Pass if you want unique prefix, **Default[False]**

		:rtype: str
		:returns: name of the file
		'''
		args = ['ffmpeg -i', '-i','-c copy -c:a aac']
		names = []
		for n in self.av:
			logg.debug(f"Downloading : {n.check('type')} : {n.format}: {n.check('qualityLabel')}")
			if status:print(f"Downloading : {n.check('type')} : {n.format}: {n.check('qualityLabel')}")
			nam = n.download(dire=dire, name=name , status=status, connection=connection, chunk=chunk, unique=unique)
			names.append(f'{nam}')
			logg.debug(f"{nam} Downloaded")
		tmp=nam.split("/")
		names.append(f'{"/".join([n for n in tmp[:-1]] + [tmp[-1][2:].split(".")[0]])}.mp4')
		cmd = [f'{n} {m}' for n,m in zip(args,names)]
		cmd = " ".join(cmd).split()

		logg.debug(f"Merge audio/video file in one file {args[-1]}")

		if self.runcmd(cmd=cmd):
			os.remove(names[0])
			os.remove(names[1])
			logg.debug(f"Video/audio downloaded and merged {args[-1]}")
			return names[-1]
		else:
			logg.error(f"Error while converting {args[0]} and {args[1]} to {args[-1]}")
			return ""



	def check_ffmpeg(self):
		'''
		Checking if FFMPEG installed or not

		:rtype: bool
		:returns: check status in (True/False)
		'''
		if "hyper fast audio and video" in self.runcmd(cmd="ffmpeg"):
			logg.debug(f"FFMPEG Found")
			return True
		return False

	def runcmd(self, cmd:str) -> str:
		'''
		Here we will run the code and return
		'''
		try:
			return str(run(cmd, capture_output=True, text=True, input='y\n')).lower()
		except FileNotFoundError:
			if cmd[0] == "ffmpeg":logg.debug(f"FFMPEG Not-Found")
			raise FFMPEG_Not_Found(f'Please install ffmpeg, check {__docs__}')
	



class Queue:
	'''
	We will manage the :class:`Stream <Stream>` queues here

	:param List[Stream] data:
		pass the dict of :class:`Stream <Stream>` objects.
	:param bool repeat:
		if you re generating Queue object from inside the function.
	
	'''
	def __init__(self,data:List[Stream], repeat:bool = False) -> None:
		self.All = sorted(data, key=lambda x: x.itag)
		self.data = data
		if not repeat:
			self.data = sorted(self.init(data),key=lambda x: x.itag)

	def __str__(self) -> str:
		return f"{self.data}"

	def __repr__(self) -> str:
		return f"{self.data}"

	def __getitem__(self, i: Union[int, slice]) -> Union[Stream, List[Stream]]:
		return self.data[i]

	@staticmethod
	def init(data:List[Stream]) -> List[Stream]:
		'''
		Here we will return the List[Stream]
		after removing 'ignore_itag'
		'''
		ignore_itag=[140]
		for n,m in enumerate(data):
			if m.itag in ignore_itag:
				del data[n]
		return data

	
	def format(self,f:str) -> "Queue":
		'''
		This will return all streams with
		format match

		:param str f:
			pass the format type ie. 'mp4'.

		:rtype: :class:`Queue <Queue>`
		:returns: :class:`Queue <Queue>` object


		'''
		return Queue(sorted([n for n in self.data if n.format == f], key=lambda x: x.check("qualityLabel")), repeat=True)

	def get_itag(self,i:int) -> Union[Stream, None]:
		'''
		This will return the stream,
		matched with i <arg>

		:param int i:
			pass the itag id for match.

		:rtype: Union[Stream, None]
		:returns: Will return :class:`Stream <Stream>` or None

		'''
		for n in self.data:
			if n.itag==i:
				return n

	@property
	def get_videos(self) -> "Queue":
		'''
		This will return all videos stream without audio.

		:rtype: :class:`Queue <Queue>`
		:returns: :class:`Queue <Queue>` object
		'''
		return Queue(sorted([n for n in self.data if n.is_video],key=lambda x: x.check("qualityLabel")), repeat=True)

	@property
	def get_audios(self) -> "Queue":
		'''
		This will return all audios stream without video.

		:rtype: :class:`Queue <Queue>`
		:returns: :class:`Queue <Queue>` object
		'''
		return Queue(sorted([n for n in self.data if n.is_audio],key=lambda x: x.check("qualityLabel")), repeat=True)

	@property
	def get_both(self) -> "Queue":
		'''
		This will return all audios/video stream.

		:rtype: :class:`Queue <Queue>`
		:returns: :class:`Queue <Queue>` object
		''' 
		return Queue(sorted([n for n in self.data if n.is_both],key=lambda x: x.check("qualityLabel")), repeat=True)


	def low(self,ff:bool=False) -> Stream:
		'''
		Low will return the lowest quality stream.

		:param bool ff:
			this input is not for the user please ignore.

		:rtype: :class:`Stream <Stream>`
		:returns: :class:`Stream <Stream>` object
		'''
		if ff:
			av = 0
			for n in range(av,av+2):
				if self.data[n].format == "webm":
					return self.data[n]
		else:return self.data[0]

	@property
	def fflow(self) -> FFMPEG:
		'''
		Processing with lowest quality video and audio

		:rtype: :class:`FFMPEG <FFMPEG>`
		:returns: :class:`FFMPEG <FFMPEG>` object
		'''
		vid = self.get_videos.low(ff=True)
		aud = self.get_audios.low(ff=True)
		return  FFMPEG([vid,aud])

	def high(self,ff:bool=False) -> Stream:
		'''
		High will return the highest quality stream.

		:param bool ff:
			this input is not for the user please ignore.

		:rtype: :class:`Stream <Stream>`
		:returns: :class:`Stream <Stream>` object
		''' 
		if ff:
			av = int(len(self.data))
			for n in range(av-2,av):
				if self.data[n].format == "webm":
					return self.data[n]
		else:return self.data[-1]
	
	@property
	def ffhigh(self) -> FFMPEG:
		'''
		Processing with highest quality video and audio

		:rtype: :class:`FFMPEG <FFMPEG>`
		:returns: :class:`FFMPEG <FFMPEG>` object
		'''
		vid = self.get_videos.high(ff=True)
		aud = self.get_audios.high(ff=True)
		return  FFMPEG([vid,aud])
	

	def mid(self,ff:bool=False) -> Stream:
		'''
		Mid will return the normal quality stream.

		:param bool ff:
			this input is not for the user please ignore.

		:rtype: :class:`Stream <Stream>`
		:returns: :class:`Stream <Stream>` object
		''' 
		if ff:
			av = int(len(self.data)/2)
			for n in range(av,av+2):
				if self.data[n].format == "webm":
					return self.data[n]
		else:return self.data[int(len(self.data)/2)]

	@property
	def ffmid(self) -> FFMPEG:
		'''
		Processing with mid quality video and audio

		:rtype: :class:`FFMPEG <FFMPEG>`
		:returns: :class:`FFMPEG <FFMPEG>` object
		'''
		vid = self.get_videos.mid(ff=True)
		aud = self.get_audios.mid(ff=True)
		return  FFMPEG([vid,aud])



	def resolution(self, quality) -> FFMPEG:
		'''
		Processing audio/video depend on resolution

		:rtype: :class:`FFMPEG <FFMPEG>`
		:returns: :class:`FFMPEG <FFMPEG>` object
		'''
		vid = ""
		for n in self.data:
			if quality == n.check("qualityLabel"):
				vid=n
				break
		if not vid:
			raise ResolutionError(f"quality {quality}p do not found")
		return  vid


	def ffresolution(self, quality:str) -> FFMPEG:
		'''
		Processing audio/video depend on resolution

		:param int quality:
			pass the quality type, Examples. ('144', '240', '360', '480', '720', '1080') more/less depend on your video.

		:rtype: :class:`FFMPEG <FFMPEG>`
		:returns: :class:`FFMPEG <FFMPEG>` object
		'''
		vid = self.get_videos.resolution(quality)
		aud = self.get_audios.mid(ff=True)
		return  FFMPEG([vid,aud])

	@property
	def all(self) -> List[Stream]:
		'''
		all will return the :class:`Stream <Stream>` objects in list

		:rtype: List of :class:`Stream <Stream>`
		:returns: list of :class:`Stream <Stream>` objects
		''' 
		return  self.All
