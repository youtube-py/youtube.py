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
	
	def download(self, dire:str="", name:str="",status:bool=False,connection:int=8, chunk:int=5120) -> Download:
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

		:rtype: :class:`Download <Download>`
		:returns: :class:`Download <Download>` object
		'''
		fname = self.filename
		if name:
			fname=name
		return Download(url=self.stream["url"], dire=dire, name=fname , status=status, connection=connection, chunk=chunk).start()


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
	def download(self,dire:str="", name:str="",status:bool=False,connection:int=8, chunk:int=5120) -> str:
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

		:rtype: str
		:returns: name of the file
		'''
		args = ['ffmpeg -i', '-i','-c copy -c:a aac']
		names = []
		for n in self.av:
			logg.debug(f"Downloading : {n.check('type')} : {n.format}: {n.check('qualityLabel')}")
			if status:print(f"Downloading : {n.check('type')} : {n.format}: {n.check('qualityLabel')}")
			nam = n.download(dire=dire, name=name , status=status, connection=connection, chunk=chunk)
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

	


# ddd=[{'itag': 18, 'mimeType': 'video/mp4', 'bitrate': 508303, 'width': 640, 'height': 360, 'lastModified': '1606480825357537', 'contentLength': '13744516', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 508202, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '216363', 'audioSampleRate': '44100', 'audioChannels': 2, 'type': 'both', 'format': 'mp4', 'codecs': 'avc1.42001E,+mp4a.40.2', 's': '8Cu8CuLcpYZ5ct0QxiKT4YDqV9m8kQF2Uu1ECYyTBckkNBICsCJBqTOoAO84hAoWLhdgTq3obNuhubWZbygDpx9KefdgIARw8JQ0qOEON', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=18&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=oi6eTA7VyMX6HR8SoVyyoeIF&gir=yes&clen=13744516&ratebypass=yes&dur=216.363&lmt=1606480825357537&mt=1606580448&fvip=6&c=WEB&txp=2310222&n=1Imq9T7-tCc2gO0ZGV3&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAKjaRpDh_jqk1D0FrgxCpmDunSeBih1uUTpB4pHUTwb9AiABquojbWbkUNYDO5z9w4v8kBCJgGS7pKV2Tes-BWpdoA%3D%3D&sig=AOq0QJ8wRAIgdfeK9xpDgybZWbuhuNbo3qTgdhLWoEh48OAoOTqBJCsCIBNkkcBTyYCN1uU2FQk8m9VqDY4TKixQ0tc5ZYpcLuC8'}, {'itag': 137, 'mimeType': 'video/mp4', 'bitrate': 4708327, 'width': 1920, 'height': 1080, 'initRange': {'start': '0', 'end': '741'}, 'indexRange': {'start': '742', 'end': '1301'}, 'lastModified': '1606480817048640', 'contentLength': '108097229', 'quality': 'hd1080', 'fps': 25, 'qualityLabel': '1080p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 3997678, 'approxDurationMs': '216320', 'type': 'video', 'format': 'mp4', 'codecs': 'avc1.640028', 's': '==w==wRfYq5cYZ6eInl4XT7hasdwhpmPlIqAhvtYlqNedoZ9DQICcr6VBe7sgVAC3AfWN-ZlgMxBYkAbR8x9rEL2laKK8TWgIQRw8JQ0qOYOF', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=137&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=108097229&dur=216.320&lmt=1606480817048640&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAJQvo9xFpPfXaaNO7MNXblBcCetwoq9m_tc3OILD2NCwAiEA0lLIxtiNSW4vSzbP6-36igJnponC4d_8IMcfRvHuQH8%3D&sig=AOq0QJ8wRQIgWT8KKal2LEr9x8RbAkYBxMglZ-NWfY3CAVgs7eBV6rcCIQD9ZodeNqlFtvhAqIlPmphwdsah7TX4lnIe6ZYc5qYfRw=='}, {'itag': 248, 'mimeType': 'video/webm', 'bitrate': 2464319, 'width': 1920, 'height': 1080, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '988'}, 'lastModified': '1606480805859703', 'contentLength': '57206066', 'quality': 'hd1080', 'fps': 25, 'qualityLabel': '1080p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 2115608, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '216320', 'type': 'video', 'format': 'webm', 'codecs': 'vp9', 's': '=w1=w1n-_21KSD52DuHfRWceQDbsXH_tDlZmhlK1_fNNetnAEiAimv4tc-ny8K1cfAxJDjDVlot8SRIwOp2VRbSNoS9tsOAhIgRw8JQ0qO1Ox', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=248&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=57206066&dur=216.320&lmt=1606480805859703&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhALiAhu9BHsXzaTXooJOHoDloXpULEPUuh2ATp6N0cuWBAiEAwv06EWqRNFtvGGZfdoJa6Gr1srGqPuwF6fD-ykdqpzM%3D&sig=AOq0QJ8wRgIhAOst9SoNSbRV2pOwIRS8tolVDjDJx1fc1K8yn-ct4vmiAiEAnteNNf_xKlhmZlDt_HXsbDQecWRfHuD25DSK12_-n1w='}, {'itag': 136, 'mimeType': 'video/mp4', 'bitrate': 2253959, 'width': 1280, 'height': 720, 'initRange': {'start': '0', 'end': '739'}, 'indexRange': {'start': '740', 'end': '1299'}, 'lastModified': '1606480817047709', 'contentLength': '50981345', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 1885404, 'approxDurationMs': '216320', 'type': 'video', 'format': 'mp4', 'codecs': 'avc1.64001f', 's': '==w==wsWVWkrnCLTaY4R5QTST2S8hoqgAOIOfYYb-mTRZRd_DQICAkpDeU0-TbxL1AcnV72mW_gfYv-AaqAF8oh5jI2bCGPgIQRw8JQ0qObOm', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=136&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=50981345&dur=216.320&lmt=1606480817047709&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhALk7gKc7Xud6LoTGXwHP8XpiFqBXF3JIS0g8aDj7FyimAiAKLKvdIbmXJAWRo9IGwnOlNnUh8dtaBqEyIko2wMsxgg%3D%3D&sig=AOq0QJ8wRQIgPGCb2Ij5ho8FAqaA-vYfg_Wm27Vncb1LxbT-0UeDpkACIQD_dRZRTm-mYYfOIOAgqoh8S2TSTQ5R4YaTLCnrkWVWsw=='}, {'itag': 247, 'mimeType': 'video/webm', 'bitrate': 1426017, 'width': 1280, 'height': 720, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '980'}, 'lastModified': '1606480805867616', 'contentLength': '33002454', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 1220504, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '216320', 'type': 'video', 'format': 'webm', 'codecs': 'vp9', 's': '=gQ=gQxG0WmzJyzjaEV-MHW1wJ2vZNIPWi3nDzmlVL8odgpAEiAAxPbbfIgdcSUFqAMfSDNreRxNyxNh_t0filTDPNEVzOAhIgRw8JQ0qOlOB', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=247&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=33002454&dur=216.320&lmt=1606480805867616&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRAIgQ4usgaIAyV5S6sq_bOG-6RlBHBLCSfiHlriRevBa7aQCID9XKN2EYEZZ1uWVDpJ0VavSsq2jKF16HhSFp7UqC0Oa&sig=AOq0QJ8wRgIhAOzVENPDTlif0t_hNxyNxRerNDSfMlqFUScdgIfbbPxAAiEApgdo8LVBmzDn3iWPINZv2Jw1WHM-VEajzyJzmW0GxQg='}, {'itag': 135, 'mimeType': 'video/mp4', 'bitrate': 1255827, 'width': 854, 'height': 480, 'initRange': {'start': '0', 'end': '740'}, 'indexRange': {'start': '741', 'end': '1300'}, 'lastModified': '1606480817062923', 'contentLength': '25831877', 'quality': 'large', 'fps': 25, 'qualityLabel': '480p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 955320, 'approxDurationMs': '216320', 'type': 'video', 'format': 'mp4', 'codecs': 'avc1.4d401e', 's': 'QKKQKKssBbMPzDNW37XLsAeRsCj0NLh-fZte06k7LytKEHIC0fyea0d0Oi1qrAexiZZTk6EeLH5qVu1gPBpx4aCR6MWgIARw8JQ0qOeO_', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=135&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=25831877&dur=216.320&lmt=1606480817062923&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAJB0f89tIXzeZqy5S1U6LwF9RkOrY2xZeiMk-D4VaexBAiEAmT58109DweOj7i6kv6T6L8P-t3o8H64ZqieVvSaCGhs%3D&sig=AOq0QJ8wRAIgWM6RCa4xpBPg1uVq5HLeE6kTZZixeerq1iO0d0aeyf0CIHEKtyL7k60_tZf-hLN0jCsReAsLX73WNDzPMbBssKKQ'}, {'itag': 244, 'mimeType': 'video/webm', 'bitrate': 717111, 'width': 854, 'height': 480, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '957'}, 'lastModified': '1606480805914016', 'contentLength': '16479361', 'quality': 'large', 'fps': 25, 'qualityLabel': '480p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 609443, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '216320', 'type': 'video', 'format': 'webm', 'codecs': 'vp9', 's': '==w==wvCsltuKey9noYJdL4KMaYZm_kbKNWdSCohWC8zIvwqDQICMSTaARMe03pSwAeVJk6ddwCUcGydjIOj9ghRKR0unQbgIQRw8JQ0qOhOq', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=244&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=16479361&dur=216.320&lmt=1606480805914016&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgVsNWt8sUJbUS4WtOxIzl0nvXyHabgJEll-rIJ-YUz8ACIQCpCZfMhdMnJlayXIp--NU_4i2I4xBH4P7rzbbqR1BVfg%3D%3D&sig=AOq0QJ8wRQIgbQnu0RKRhg9jOIjdyGcUCwdd6kJVehwSp30eMRAaTSMCIQDqwvIz8CWqoCSdWNKbk_mZYaMK4LdJYon9yeKutlsCvw=='}, {'itag': 134, 'mimeType': 'video/mp4', 'bitrate': 594687, 'width': 640, 'height': 360, 'initRange': {'start': '0', 'end': '740'}, 'indexRange': {'start': '741', 'end': '1300'}, 'lastModified': '1606480817054720', 'contentLength': '12073634', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 446510, 'highReplication': True, 'approxDurationMs': '216320', 'type': 'video', 'format': 'mp4', 'codecs': 'avc1.4d401e', 's': '-7I-7Ir4h-3GjOrgTR4zZdxdGgbQuOg1dWVM0VCCFYQxpBICIPp7LF6fmhfVNAxh37lrsW4jGQveCXBIBsS6jm21JlfgIARw8JQ0qOMO_', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=134&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=12073634&dur=216.320&lmt=1606480817054720&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAJbsaDlTRQK2g3XGFXXH0DwI58hyk5Nvyovj3Zj5g-fAAiEA57jz1vSgrzPyzdlI4aSWbAmFkyGiIlYHTyRzsOLj78Y%3D&sig=AOq0QJ8wRAIgflJ12mj6SsBIBXCevQGj4Wsrl73hxMNVfhmf6FL7pPICIBpxQYFCCV0_VWd1gOuQbgGdxdZz4RTgrOjG3-h4rI7-'}, {'itag': 243, 'mimeType': 'video/webm', 'bitrate': 380122, 'width': 640, 'height': 360, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '957'}, 'lastModified': '1606480805968597', 'contentLength': '8903757', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 329280, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '216320', 'type': 'video', 'format': 'webm', 'codecs': 'vp9', 's': '==g==gCercLOBTkU5OOImbjt2mtnk2iz_tHPkKmtfAwOX2iIAiAl003NoBI0ZHa8zAXon8LN-ePLXYw_9vImvWzyQ1MgEKAhIQRw8JQ0qOtOb', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=243&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=8903757&dur=216.320&lmt=1606480805968597&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgQxDWJ0AscWe_ydeit8R1ECPLOrvb3gKEZjWPBp040UQCIQC4BYpx_xDR8txUEUXH2SGWoLxmbUBmr0CIn-tLe8681Q%3D%3D&sig=AOq0QJ8wRQIhAKEgM1QyzWvmIv9_wYXLPe-NL8noXtz8aHZ0IBoN300lAiAIi2XOwAfbmKkPHt_zi2kntm2tjbmIOO5UkTBOLcreCg=='}, {'itag': 133, 'mimeType': 'video/mp4', 'bitrate': 259406, 'width': 426, 'height': 240, 'initRange': {'start': '0', 'end': '739'}, 'indexRange': {'start': '740', 'end': '1299'}, 'lastModified': '1606480817053058', 'contentLength': '5742765', 'quality': 'small', 'fps': 25, 'qualityLabel': '240p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 212380, 'approxDurationMs': '216320', 'type': 'video', 'format': 'mp4', 'codecs': 'avc1.4d4015', 's': '=Qe=Qez_YZgmXKsfP7LAVNF4DSjvY0WG3-DrgWIfb4WYYrvAEiA-gf1hgzWNRPVR3AOfD7_uPSFzKTSu2nzUx9E2ARTHRJAhIgRw8JQ0qOfOB', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=133&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=5742765&dur=216.320&lmt=1606480817053058&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAP6mFT4jeS8cJCEdg3Ru-iOclN49bULRGP3LyYB2QG-1AiALPFet8Y44sFYLQVyIHbfTmSEI5CUEwdygBFdpjSevlA%3D%3D&sig=AOq0QJ8wRgIhAJRHTRA2E9xUzn2uSTKzFSPu_7DfOf3RVPRNWzgh1fg-AiEAvrYYW4bBIWgrD-3GW0YvjSD4FNVAL7PfsKXmgZY_zeQ='}, {'itag': 242, 'mimeType': 'video/webm', 'bitrate': 203358, 'width': 426, 'height': 240, 'initRange': {'start': '0', 'end': '218'}, 'indexRange': {'start': '219', 'end': '956'}, 'lastModified': '1606480805856031', 'contentLength': '4775218', 'quality': 'small', 'fps': 25, 'qualityLabel': '240p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 176598, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '216320', 'type': 'video', 'format': 'webm', 'codecs': 'vp9', 's': '==A==A5fK-T6vVEohgEZi2-iY0U1jdBS1IeRyLGJ4fAYWjLlDQIC86sAf2rpnAR05AOxamYqlbPn59j771UO2z4cy5JLgeNgIQRw8JQ0qOJOZ', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=242&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=4775218&dur=216.320&lmt=1606480805856031&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhANDQIB2K36i1oXVdW6rvDljUOlNYUJSmsawFyyoppXOXAiBLMJbtpB0t2083lc1eKWBTOuc-hpTws63ij5Q5s3bJ4Q%3D%3D&sig=AOq0QJ8wRQIgNegLJ5yc4z2OU177j95nPblqYmaxOJ50RAnpr2fAs68CIQDlLjWYAf4ZGLyReI1SBdj1U0Yi-2iZEghoEVv6T-Kf5A=='}, {'itag': 160, 'mimeType': 'video/mp4', 'bitrate': 116016, 'width': 256, 'height': 144, 'initRange': {'start': '0', 'end': '738'}, 'indexRange': {'start': '739', 'end': '1298'}, 'lastModified': '1606480817072996', 'contentLength': '2414363', 'quality': 'tiny', 'fps': 25, 'qualityLabel': '144p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 89288, 'approxDurationMs': '216320', 'type': 'video', 'format': 'mp4', 'codecs': 'avc1.4d400c', 's': '=Qq=Qq-a21oI6toil4Kg4JIuqOTL3X5xlexX6q8Cnu60z06AEiA5Ir8E7Xx3RHQgeA55qBKeW7VAi8-bK7bRdMURLOJvFIAhIgRw8JQ0qOCOg', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=160&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=2414363&dur=216.320&lmt=1606480817072996&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAPuJFRShk-NBokCaEQfMQNYHLCU8xzvaRuVhOiigx2skAiEAgbGKdR6BfZ2YGlFx1MLNDh2_PI6AWLtTqpmheD92FG4%3D&sig=AOq0QJ8wRgIhAIFvJOLRUMdRb7Kb-8iAV7WeKBq55CegQHR3xX7E8rI5AiEA60z06ung8q6Xxelx5X3LTOquIJ4gK4liot6Io12a-qQ='}, {'itag': 278, 'mimeType': 'video/webm', 'bitrate': 93329, 'width': 256, 'height': 144, 'initRange': {'start': '0', 'end': '218'}, 'indexRange': {'start': '219', 'end': '955'}, 'lastModified': '1606480805842854', 'contentLength': '2265367', 'quality': 'tiny', 'fps': 25, 'qualityLabel': '144p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 83778, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '216320', 'type': 'video', 'format': 'webm', 'codecs': 'vp9', 's': '=sB=sBG08NSG5TjGPOlQWhGCV0f4FL6mDchBAaDxIR3fPu1AEiABHWRS2Ti6ny6jWA_-XpE2gg-NZQeKJhe76jmuwRgQ5MAhIgRw8JQ0qOxOV', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=278&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=video%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=2265367&dur=216.320&lmt=1606480805842854&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2316222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAPj5ESuvIdewMGAAd1DzH3IC4h5_HjxhR7uLhI1NCDsVAiEAhRmqliL-uQrFIU5NC3eMJuoZxyVmmeP0Er5-Ave0tBU%3D&sig=AOq0QJ8wRgIhAM5QgRwumj67ehJKeQZN-gg2EpX-_xWj6yn6iT2SRWHBAiEA1uPf3RIVDaABhcDm6LF4f0VCGhWQlOPGjT5GSN80GBs='}, {'itag': 140, 'mimeType': 'audio/mp4', 'bitrate': 130540, 'initRange': {'start': '0', 'end': '631'}, 'indexRange': {'start': '632', 'end': '927'}, 'lastModified': '1606480816199826', 'contentLength': '3503048', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 129524, 'highReplication': True, 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '216363', 'audioSampleRate': '44100', 'audioChannels': 2, 'loudnessDb': 5.6000004, 'type': 'audio', 'format': 'mp4', 'codecs': 'mp4a.40.2', 's': 't4kt4kOcUnNQTNcCi032JLSQRbeaF9sJgF81_ha6-oOU-AICAFw34g-EFpdG4AIS_Ej6F3qIP6706OT2l-OrjcGI4ZLgIARw8JQ0qO1OZ', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=140&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=audio%2Fmp4&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=3503048&dur=216.363&lmt=1606480816199826&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2311222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgeBDhOu6PUA8h3lub9xVLCCY8n-MoCXIwOHcH_TjQUb0CIQD75E9pkSyZqCzArNz-8FuNmxqnZiNtvzrVU-iZA6UXaQ%3D%3D&sig=AOq0QJ8wRAIgLZ4IGcjrO-l2TO6076PIq3F6jE_SI14GdpFE-g43wFACIA-UOo-6ah_Z8FgJs9FaebRQSLJ230iCcNTQNnUcOk4t'}, {'itag': 249, 'mimeType': 'audio/webm', 'bitrate': 61069, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '629'}, 'lastModified': '1606480801923738', 'contentLength': '1548903', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 57276, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '216341', 'audioSampleRate': '48000', 'audioChannels': 2, 'loudnessDb': 5.5900002, 'type': 'audio', 'format': 'webm', 'codecs': 'opus', 's': '==A==AC1mcvc5-1V5NoKZBiSEBMbSvihWIqO-VkNSvwlq6czCQICkjy8TG-tZFog6AM0wdJ-RIlmagZNwoN8C_wPk3lr7_IgIQRw8JQ0qONOP', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=249&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=audio%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=1548903&dur=216.341&lmt=1606480801923738&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2311222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAOiDDe27rmdUNNs-epLIbTEFoBG0mzX4c_lD-WVk1TYiAiAK9VkOz6CMmRYGGKb0wMKRZCfrEXQ1jpnHjW0bh2mpig%3D%3D&sig=AOq0QJ8wRQIgI_7rl3kPw_C8NowNZgamlIR-Jdw0MN6goFZt-GT8yjkCIQCzc6qlwvSPkV-OqIWhivSbMBESiBZKoN5V1-5cvcm1CA=='}, {'itag': 250, 'mimeType': 'audio/webm', 'bitrate': 79396, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '629'}, 'lastModified': '1606480802443010', 'contentLength': '2023978', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 74843, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '216341', 'audioSampleRate': '48000', 'audioChannels': 2, 'loudnessDb': 5.5900002, 'type': 'audio', 'format': 'webm', 'codecs': 'opus', 's': '==Q==QAnkUwmFvcgFvBSzYUs5sjwu5iS86WgK2zUX9W5WeqYAiAzHsYKOl8eMhUzzA6Bg0RQ69BQ0RfMhpI1F6hLJle00PAhIQRw8JQ0qOUOf', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=250&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=audio%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=2023978&dur=216.341&lmt=1606480802443010&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2311222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRAIgVM6eli5OhRaIwvcX1u777pf5dgLDmX2QdPIhBBKNw08CICQzymOPsCFvy0R7MCg5me3tWjzLdEJ4uoCb7cuIybBt&sig=AOq0QJ8wRQIhAP00elJLh6F1IphMfR0QB96QR0gB6UzzUhMe8lOKYsHzAiAYqeW5W9Xfz2KgW68Si5uwjs5sUYzSBvFgcvFmwUknAQ=='}, {'itag': 251, 'mimeType': 'audio/webm', 'bitrate': 151452, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '629'}, 'lastModified': '1606480802588428', 'contentLength': '3903186', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 144334, 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '216341', 'audioSampleRate': '48000', 'audioChannels': 2, 'loudnessDb': 5.5900002, 'type': 'audio', 'format': 'webm', 'codecs': 'opus', 's': '=op=opNOFMMh9DAAlZNrmAEPyMd-vWMqBUcqnxU9Wdk6ltkAEiAoJTbpBktBRa-bTAMODo8R3Cx2hGknSzAP8QIuiozhPNAhIgRw8JQ0qO9Oo', 'sp': 'sig', 'url': 'https://r6---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606602349&ei=DXrCX4HYNsiwvQT6spfADA&ip=171.60.177.128&id=o-AFM4ZIRW6CXAcAMmIo499CWyIp_1F0RrUIOirOhdWA9c&itag=251&source=youtube&requiressl=yes&mh=YA&mm=31%2C29&mn=sn-ci5gup-civl%2Csn-ci5gup-cvhk&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=696250&vprv=1&mime=audio%2Fwebm&ns=DNCmEBtXb1sJZ_fUaL0Hm4cF&gir=yes&clen=3903186&dur=216.341&lmt=1606480802588428&mt=1606580448&fvip=6&keepalive=yes&c=WEB&txp=2311222&n=gkVd_Bk54e6S10gEAhN&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAPmUI7Y8f0OG27FsqT8mfKotv5ugpW-4fYReKyeC-g2kAiABXHbVv7sespnudprx0M3G7NgusVQ08MQwMcKoBrZWkg%3D%3D&sig=AOq0QJ8wRgIhANPhzoiuIQ8PAzSnkGh2xC3R8oDOM9Tb-aRBtkBpbTJoAiEAktl6kdWoUxnqcUBqMWv-dMyPEAmrNZlAAD9hMMFONpo='}]
# dtt=[]
# for n in ddd:
# 	dtt.append(Stream(n,"testinga"))


# # # print(Queue(dtt).format("mp4").Last.Url)

# # # for n in Queue(dtt).get_videos.get_itag(160):
# # # 	print(n)


# print(Queue(dtt).ffmid)


