# -*- coding: utf-8 -*-
"""
Here are some function which helps extracting info
online information <GET requests>

"""
from typing import Union, Callable
from typing import List, Tuple 
from typing import Dict
from typing import Any
from .Connection import HTTP
from re import compile, findall
from urllib.parse import unquote
import json, logging
from .Error import (RegexError, VideoInfo, GeoBlockingError, ParsecError, GoogleReCaptchaError)
from .Config import (__issues__,__github__)

logg = logging.getLogger(__name__)

def Get_js(req:HTTP,vid:str) -> Tuple[str, str]:
	'''
	Thie will return the url of base.js
	
	Example..
	>>> Get_Js("M3mJkSqZbX4")
	'https://www.youtube.com/s/player/XXXXXXXXX/player_ias.vflset/en_GB/base.js'
	'''
	data=req._GET(f'https://www.youtube.com/watch?v={vid}').text
	try:
		match=compile(r'<script  src="(.*?)" type="text/javascript" name="player_ias/base" ></script>')
		src=findall(match,data)[0]
	except:
		match=compile(r'jsUrl":"(.*?)"')
		url = findall(match,data)
		if url:
			src = url[0]
		else:
			raise GoogleReCaptchaError()
	if src:
		return "https://www.youtube.com"+src, data
		logg.debug("Successfully got raw js <player_ias/base.js>")
	else:
		logg.error(f"Error raw js <player_ias/base.js> not found <VID:{vid}>")
		raise RegexError(f"base.js not found please report here {__issues__} with {vid}, help us make it more stable for everyone")

def Is_age_restricted(rawhtml:str) -> bool:
	'''
	This will return true or False

	>>> is_age_restricted(htmldata)
	True/False


	'''
	if "og:restrictions:age" in rawhtml:
		return True
	return False

def Get_video_info(req:HTTP,url:str) -> Tuple[Any, bool, Dict[str, str]]:
	'''
	This willl return video info 
	from: https://youtube.com/get_video_info

	:args str url
		url in string <get_video_info>

	:rtype: Tuple[Any, bool, Dict[str, str]]
	:returns: the extracted data, true if signature found, raw data dict
	'''
	try:
		r=req._GET(url).text
		Fdata = {unquote(o.split("=")[0]):unquote(o.split("=")[1]) for o in r.split("&")}
		data = json.loads(Fdata["player_response"])
		r = data = json.loads(Fdata["player_response"]) # to return this  
		assert CheckPlayable(data["playabilityStatus"]) == True, f'Video is {data["playabilityStatus"]["status"]}, Please use Proxy/VPN to bypass Geo-blocking'
		data = GetStreamingData(data["streamingData"])
		# data = data["streamingData"]["adaptiveFormats"] + data["streamingData"]["formats"]
		issig:bool = Videodata_parse(data)
		logg.debug(f"We Successfully received video data/info")
		return data, issig, r
	except:
		logg.error(f"Video Info not found <{url}> please contact <{__issues__}>")
		raise VideoInfo(f"Video Info not found <{url}> please contact <{__issues__}>, help us make it more stable for everyone")
def Videodata_parse(data:Dict[Any, Any]) -> bool:
	'''
	Takes Data and parsec the signatureCipher
	and upadte the url and del the signatureCipher
	if it has or return the same
	'''
	logg.debug(f"Videodata processing ..... ")
	sig:bool=False
	for n in data:
		if "signatureCipher" in n.keys():
			sig=True
			url = _parsesignatureCipher(n["signatureCipher"])
			del n["signatureCipher"]
			n.update(url)
		else:
			sig=False
			continue
	logg.debug(f"Videodata processing Completed, Signature found: <{sig}> ")
	return sig

def _parsesignatureCipher(signatureCipherraw:str) -> Dict[Any, Any]:
	'''
	this will convert the str of signatureCipher
	to dict and return
	'''
	data={unquote(o.split("=")[0]):unquote(o.split("=")[1]) for o in signatureCipherraw.split("&")}
	return data


def Req_get(req:HTTP,url:str) -> str:
	'''
	Send simple get request with object
	'''
	return req._GET(url).text

def CheckPlayable(data:Dict[Any, Any]) -> bool:
	'''
	Here we will check is video is really
	playable or not/ Check if video is aviable
	for you or in your country.
	'''
	if data["status"] !="OK":
		logg.info(f'Video is {data["status"]}')
		raise GeoBlockingError(f'Video is {data["status"]}, {data["errorScreen"]["playerErrorMessageRenderer"]["subreason"]["runs"][0]["text"].replace("+"," ")}')
		return False
	return True


def GetStreamingData(data:Dict[Any, Any]) -> List[Any]:
	'''
	This will return all the streams with or without audio streams, ``adaptiveFormats`` and ``formats``.
	'''
	d=[]

	for n in data["formats"]:
		mtype, vcode=n["mimeType"].split(";+")
		n["mimeType"] = mtype
		mtype, forma = mtype.split("/")
		key, value = vcode.split("=")
		n["type"] = "both"
		n["format"] = forma
		n[key] = value.replace('"',"")
		d.append(n)

	for n in data["adaptiveFormats"]:
		mtype, vcode=n["mimeType"].split(";+")
		n["mimeType"] = mtype
		mtype, forma = mtype.split("/")
		key, value = vcode.split("=")
		n["type"] = mtype
		n["format"] = forma
		n[key] = value.replace('"',"")
		d.append(n)

	return d


def Get_playlist_videos(http:HTTP, url:str) -> Dict[str,str]:
	'''
	This will parse the initial json dict from web page source.

	:param HTTP http:
		 Pass the :class:`HTTP <HTTP>` object.
	:param str url:
		pass the plsylist url

	:rtype: Dict[str,str]
	:returns: The dict of of video details 
	'''
	html = http._GET(url).text.replace("\n","")
	f = ""
	try:
		match = compile(r'window\["ytInitialData"\] = (.*?);')
		f = findall(match, html)[0]
	except:
		match = compile(r'var ytInitialData = (.*?);')
		f = findall(match, html)[0]


	if f:
		return json.loads(f)
	else:
		logg.debug(f'RegexError we cannot found {match}')
		raise RegexError(f'RegexError we cannot found {match}')
	

def Continuation(http:HTTP,videos:List[Dict[str,str]], token:str) -> str:
	'''
	This will extract the data we will get from **browse_ajax** API.

	:param HTTP http:
		Pass the :class:`HTTP <HTTP>` object.
	:param List[Dict[str,str]] videos:
		Pass the videos dicts list.
	:param str token:
		Pass the token if any.

	:rtype: str
	:returns: The new/next continuous token if available.
	'''
	params = {
		"ctoken": token
	}
	headers={
		'X-YouTube-Client-Name': '1',
		'X-YouTube-Client-Version': '2.20200720.00.02'
	}
	token = ""
	data = http._GET("https://www.youtube.com/browse_ajax",params=params,headers=headers).json()[-1]
	for n in data["response"]["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]:
		if "playlistVideoRenderer" in n.keys():
			tmp = dict()
			tmp["vid"] = n["playlistVideoRenderer"]["videoId"]
			tmp["name"] = n["playlistVideoRenderer"]["title"]["runs"][0]["text"]
			videos.append(tmp)
		elif "continuationItemRenderer" in n.keys():
			token = n["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
		else:
			raise ParsecError(f'Serious Bug please report here {__issues__}')

	return token

def Parse_search_json(data:Dict[str,str], videos:List[Dict[str,str]]) -> bool:
	# print(json.dumps(data))
	for n in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]:
		try:
			det = n["videoRenderer"]
			videos.append(dict(vid=det["videoId"],name=det["title"]["runs"][0]["text"]))
		except:
			continue
	return True



def Search_results(http:HTTP, query:str, videos:List[Dict[str,str]],country:str) -> bool:
	'''
	This will parse the initial json dict from web page source.
	
	:param HTTP http:
		Pass the :class:`HTTP <HTTP>` object.
	:param str query:
		pass query for searching.
	:param str videos:
		pass the video list of dicts
	:param str country:
		pass the country code

	:rtype: bool
	:returns: true or false depend on search results.

	'''
	SEARCH_URL = "https://www.youtube.com/results"
	PARAMS = {
		"search_query":query,
		"gl":country.upper()
	}
	HEADERS = {}

	html = http._GET(SEARCH_URL, params=PARAMS,headers=HEADERS).text.replace("\n","")
	try:
		match = compile(r'var ytInitialData = (.*?);')
		f = findall(match, html)[0]
		f = json.loads(f)
	except:
		logg.debug(f'RegexError we cannot found {match}')
		raise RegexError(f'RegexError we cannot found {match}')

	if f:
		if Parse_search_json(f,videos):
			return True
		else:
			return False
