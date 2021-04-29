[![banner](https://github.com/youtube-py/youtube.py/raw/master/img/header.png)](https://youtube-python.mayankfawkes.xyz/)

![rtd](https://readthedocs.org/projects/youtube-python/badge/?version=latest)
![size](https://img.shields.io/github/languages/code-size/youtube-py/youtube.py)
![ver](https://img.shields.io/pypi/pyversions/youtube.py)
![lang](https://img.shields.io/github/languages/top/youtube-py/youtube.py)
![status](https://img.shields.io/pypi/status/youtube.py)
![ver](https://img.shields.io/pypi/v/youtube.py)
[![Downloads](https://pepy.tech/badge/youtube-py/week)](https://pepy.tech/project/youtube-py)

# YouTube Python

Youtube Python is best and powerful python module for developers internal use APIs or command line CLI , Downloading specific video or playlist if now easy.

# Install

## Python module
run this command on terminal.

```
$ pip install -U youtube.py
```

Have multipls versions of python?

```
$ python3.x -m pip install -U youtube.py
```

## Install FFMPEG

Windows download [link](https://ffmpeg.org/download.html). After download the exe file make sure to put that on environment variables or simply move ``ffmpeg.exe`` to ``c:\windows\system32\``

For Linux

```
$ sudo apt update
$ sudo apt install ffmpeg
```



# Features

* Supports proxy (for scraping data, proxy will not be used for downloading videos)
* Rate limit bypass
* Light module
* Command line input available
* Supports FFMPEG
* Can parsec youtube video details
* Youtube Search, Video, PlayList

# Basic

```python
from youtube import Video

video_url = "https://www.youtube.com/watch?v=3AtDnEC4zak"

v = Video(video_url)

#Print Title
print(v.title)

#Print Author name
print(v.author)

#Print Channel ID
print(v.channel)

#Print video description
print(v.description)

#Print video length in second
print(v.length)

#Print video keywords in dict
print(v.keywords)

#Print high resolution thumbnail
print(v.thumbnail)

#Print video id
print(v.videoId)

#Print total video views
print(v.views)
```

Working with streams

```python
>>> from youtube import Video
>>> v = Video("https://www.youtube.com/watch?v=3AtDnEC4zak")
>>> v.title
"Charlie Puth - We Don't Talk Anymore (feat. Selena Gomez) [Official Video]"
>>> v.length
231
>>> v.views
2550001850
>>> v.streams
[<Class Stream: itag="18" qualityLabel="360p" fps="24" mime="video/mp4" type="both" format="mp4" codecs="avc1.42001E,+mp4a.40.2">, 
<Class Stream: itag="133" qualityLabel="240p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="avc1.4d4015">, 
<Class Stream: itag="134" qualityLabel="360p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="avc1.4d401e">, 
<Class Stream: itag="135" qualityLabel="480p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="avc1.4d401e">, 
<Class Stream: itag="136" qualityLabel="720p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="avc1.4d401f">, 
<Class Stream: itag="137" qualityLabel="1080p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="avc1.640028">, 
<Class Stream: itag="160" qualityLabel="144p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="avc1.4d400c">, 
<Class Stream: itag="242" qualityLabel="240p" fps="24" mime="video/webm" type="video" format="webm" codecs="vp9">, 
<Class Stream: itag="243" qualityLabel="360p" fps="24" mime="video/webm" type="video" format="webm" codecs="vp9">, 
<Class Stream: itag="244" qualityLabel="480p" fps="24" mime="video/webm" type="video" format="webm" codecs="vp9">, 
<Class Stream: itag="247" qualityLabel="720p" fps="24" mime="video/webm" type="video" format="webm" codecs="vp9">, 
<Class Stream: itag="248" qualityLabel="1080p" fps="24" mime="video/webm" type="video" format="webm" codecs="vp9">, 
<Class Stream: itag="249" bitrate="59056" mime="audio/webm" type="audio" format="webm" codecs="opus">, 
<Class Stream: itag="250" bitrate="76035" mime="audio/webm" type="audio" format="webm" codecs="opus">, 
<Class Stream: itag="251" bitrate="143852" mime="audio/webm" type="audio" format="webm" codecs="opus">, 
<Class Stream: itag="278" qualityLabel="144p" fps="24" mime="video/webm" type="video" format="webm" codecs="vp9">, 
<Class Stream: itag="394" qualityLabel="144p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="av01.0.00M.08">, 
<Class Stream: itag="395" qualityLabel="240p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="av01.0.00M.08">, 
<Class Stream: itag="396" qualityLabel="360p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="av01.0.01M.08">, 
<Class Stream: itag="397" qualityLabel="480p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="av01.0.04M.08">, 
<Class Stream: itag="398" qualityLabel="720p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="av01.0.05M.08">, 
<Class Stream: itag="399" qualityLabel="1080p" fps="24" mime="video/mp4" type="video" format="mp4" codecs="av01.0.08M.08">]
>>> type(v.streams)
<class 'youtube.Stream.Queue'>
>>> v.thumbnail
'https://i.ytimg.com/vi/3AtDnEC4zak/maxresdefault.jpg'
>>> v.get_dict
[{'itag': 18, 'mimeType': 'video/mp4', 'bitrate': 395026, 'width': 640, 'height': 360, 'lastModified': '1580859977121104', 'contentLength': '11378647', 'quality': 'medium', 'fps': 24, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 394913, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '230504', 'audioSampleRate': '44100', 'audioChannels': 2, 'type': 'both', 'format': 'mp4', 'codecs': 'avc1.42001E,+mp4a.40.2', 's': 'mAq0QJ8wRQIgRe0DKBgGi4uiqHOk6dmrhwQKtFCcrhCKAvNHps-hzk0CIQDDW_HSmfLlD3-4G5x3XtamqDtAWRVkjYYGv_qFYUY4Ow====', 'sp': 'sig', 'url': 'https://r7---sn-ci5gup-civl.googlevideo.com/videoplayback?expire=1606933954&ei=YonHX_XTBIKqvQSXv4-QDg ...........
```
# Command Line Input


```bash
usage: youtube [-h] [-o OUTPUT] [-l] [-ff [FFMPEG] | -v [VIDEO] | -i ITAG | -s
               | -a [AUDIO] | -r [RESOLUTION] | --version]
               url

Definitions:
  Quality Types: ('HIGH','MID', 'LOW')
  Video resolution examples. ('144', '240', '360', '480', '720', '1080') more/less depend on your video

Note:
  Default values for '--ffmpeg', '--video', '--audio' is 'HIGH'
  Default values for '--resolution' is 720

positional arguments:
  url                   Enter video or playlist url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output location for downloading streams.
  -l, --logs            To enable extra logs.
  -ff [FFMPEG], --ffmpeg [FFMPEG]
                        FFMPEG downloads audio/video both then copy in one file, Pass the quality type.
  -v [VIDEO], --video [VIDEO]
                        Downlaod video (only progressive), Pass quality.
  -i ITAG, --itag ITAG  Download stream with itag, Pass itag id.
  -s, --streams         This argument will list the all available streams.
  -a [AUDIO], --audio [AUDIO]
                        Download audio, Pass quality.
  -r [RESOLUTION], --resolution [RESOLUTION]
                        Download stream with quality type, Pass video resolution.
  --version             Check the current version of youtube.py

```
# Sample Codes
Here are some sample codes.

## How to download mass videos with ffmpeg.
```python
from youtube import Video

video_url = ["3AtDnEC4zak", "3AtDnEC4zak"]

for vdo in video_url:
        v = Video(f"https://youtu.be/{vdo}").streams
        v.ffhigh.download() # ffhigh will download stream with highest quality

```
## How to download all playlist videos concurrently/fast.
```python
from youtube import PlayList
import concurrent.futures


MAX_CONCURRENT_DOWNLOADS = 1 #max concurrent download at ones

video_url = "https://www.youtube.com/playlist?list=PLeXILI4F6_4XJau4ZlJXD7-K75g6rDebr"

p = PlayList(video_url, process=True) # process=True to generate all Video objects

func = lambda x: x.streams.get_audios.low().download()

with  concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
        for n in executor.map(func,p.get_object):
                print(f'{n} Downloaded')
```
## Contributing

You just simple fork the project from github and fix the bugs and push with full explanation of bug and fix.

We do love when you invest your time and contribute us for making us more better/stable.

Your each bug report on github or contribute is much appreciated


