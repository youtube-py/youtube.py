# -*- coding: utf-8 -*-
"""
Here are some function which helps extracting info
offline infomation parsec/filter/sort
"""
from typing import Union, Callable
from typing import List, NoReturn
from typing import Dict
from typing import Any
import logging
from re import compile, findall
from urllib.parse import unquote
from .Cipher import Cipher
from .Config import (__issues__,__github__)
from .Error import (InvalidVideoUrl, ParsecError)


logg = logging.getLogger(__name__)


def Get_video_id(url:str) -> str:
	'''
	Thie will return this video ID '&v='
	
	Example..

	>>> Get_Video_id("https://www.youtube.com/watch?v=12345678")
	'12345678'
	'''
	fu:str=""
	if "youtube.com" in url:
		fu={n.split("=")[0]:n.split("=")[1] for n in Get_url(url).split("?")[1].split("&")}["v"]
	elif "youtu.be" in url:
		fu=url.split("/")[-1]
	else:
		fu=""

	if fu:
		logg.debug(f"We successfully extracted VID<{fu}> from <{url}>")
		return fu
	else:
		logg.info(f'We dont support this url <{url}> please enter valid youtube watch url or contact {__issues__}')
		raise InvalidVideoUrl(f'We dont support this url <{url}> please enter valid youtube watch url or contact {__issues__}')

def Get_url(url:str) -> str:
	'''
	This will decode the url
	
	Example..

	>>> Get_Url("https://www.youtube.com/watchv%3D9NQqaKz7eyI")
	'https://www.youtube.com/watchv=9NQqaKz7eyI'
	'''
	return unquote(url)

def Get_vid_info_url(vid:str,whaturl:str) -> str:
	'''
	This will return the valid url of get_video_info

	The url for Video information do not works on 18+
	Videos

	:param str vid: 
		Pass the video id.
	:parma str whaturl:
		Pass the video url.

	:rtype: str
	:returns: the data url
	'''
	params={
		"video_id":vid,
		"ps":"default",
		"eurl":whaturl,
		"hl":"en_US",
		"html5": "1",
                "c": "TVHTML5",
                "cver": "6.20180913"
	}
	return "https://youtube.com/get_video_info?"+"&".join(f"{n}={m}" for n,m in params.items())
	
def Get_r_vid_info_url(vid:str) -> str:
	'''
	This will return the valid url of get_video_info

	The url for Video information do works on 18+ Videos

	:param str vid: 
		Pass the video id.

	:rtype: str
	:returns: the data url
	'''
	params={
		"video_id":vid,
		"eurl":f"https://youtube.googleapis.com/v/{vid}",
		"sts":"",
		"html5": "1",
                "c": "TVHTML5",
                "cver": "6.20180913"
	}
	return "https://youtube.com/get_video_info?"+"&".join(f"{n}={m}" for n,m in params.items())

def Decipher_signature(data:Dict[Any, Any],js:str) -> None:
	'''
	Here we will add the signature to url <&sig>

	:param dict data:
		All possible streams. 
	:param str js:
		Raw base.js js.

	:rtype: None
	:returns: nothing
	'''
	logg.debug("Decipher signature... ")

	enc=Cipher(js)
	for i,n in enumerate(data):
		if "&sig" in n["url"]:
			logg.debug("Video url already have signature token")
			continue
		sig=enc.Get_signature(n["s"])
		data[i]["url"] = n["url"] + "&sig=" + sig

	logg.debug("successfully Decipher signature... ")


#Playlist functions
def Get_playlist_id(url:str) -> str:
	'''
	Pass url of playlist and we will return the ID

	:param str url:
		pass the playlist url

	:rtype: str
	:returns: The params [**list**] from url.
	'''
	return {n.split("=")[0]:n.split("=")[1] for n in Get_url(url).split("?")[1].split("&")}["list"]


def Extract_from_web_json(data:Dict[str,str]) -> Dict[str,str]:
	'''
	This will extract the data we will get from website.

	:param Dict[str,str] data:
		Dict data of videos.

	:rtupe: Dict[str,str]
	:returns: the video ids dict with name. ``{"vid": "","name",""}``
	'''
	vids = []
	token = None

	for n in data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["playlistVideoListRenderer"]["contents"]:
		if "playlistVideoRenderer" in n.keys():
			tmp = dict()
			tmp["vid"] = n["playlistVideoRenderer"]["videoId"]
			tmp["name"] = n["playlistVideoRenderer"]["title"]["runs"][0]["text"]
			vids.append(tmp)
		elif "continuationItemRenderer" in n.keys():
			token = n["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
		else:
			raise ParsecError(f'Serious Bug please report here {__issues__}')

	return vids, token
