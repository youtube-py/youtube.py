.. _basic:

Basic Codes
===========

Class Video
-----------

**Sample code for Video class overview**

.. code-block:: python

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




**Streams of Video class overview**

.. code-block:: python

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



Class PlayList
---------------

.. code-block:: python

	>>> from youtube import PlayList, HIGH
	>>> p = PlayList("https://www.youtube.com/playlist?list=PLeXILI4F6_4XJau4ZlJXD7-K75g6rDebr")
	>>> p.get_dict
	[{'vid': 'C-p3HnovSbU', 'name': 'Top ABBA Songs Playlist   #ABBA Best Mix'}, 
	{'vid': 'u44-KMrI4Hk', 'name': 'Top 100 Traditional Christmas Songs Ever - Best Classic Christmas Songs 2021 Collection'}, 
	{'vid': 'KOICR55wlGY', 'name': 'Merry Christmas 2021 ☃️ Beautiful Traditional Christmas Songs Playlist ☃️Classic Christmas Songs'}, 
	{'vid': 'jiV7hyX65BM', 'name': 'ABBA GOLD GREATEST HITS - ABBA FULL ALBUM PLAYLIST'}, 
	{'vid': 'Q3YkR_Eyh-s', 'name': 'Best Christmas Songs Playlist 2020 - Top 10 Christmas Songs || Merry Christmas Music Of All Time'}, 
	{'vid': 'fmfy9-Z4ZLc', 'name': 'Best Songs Of ABBA Collection 2020 | ABBA Greatest Hits Full Album'}, 
	{'vid': '-PJDukRSHis', 'name': 'ABBA Best Songs Collection 2020 | Greatest Hits New Playlist Of ABBA'}, 
	{'vid': 'ptaok2DmN0Y', 'name': 'Christmas 2020 🎁 Christmas Songs 2020 - 2021 🎄 Nonstop Christmas Songs Medley 2020 - 2021'}, 
	{'vid': 'dLU23pGXNF8', 'name': 'NEW ABBA Full Album Playlist  || The Very Best Song #ABBA GOLD'}]
	>>> p.get_object
	[<Class Video VID=C-p3HnovSbU PROXY=None ID=0 NAME=Top ABBA Songs Playlist   #ABBA Best Mix 0x7f34987cd2d0>, 
	<Class Video VID=u44-KMrI4Hk PROXY=None ID=1 NAME=Top 100 Traditional Christmas Songs Ever - Best Classic Christmas Songs 2021 Collection 0x7f34987cdcd0>, 
	<Class Video VID=KOICR55wlGY PROXY=None ID=2 NAME=Merry Christmas 2021 ☃️ Beautiful Traditional Christmas Songs Playlist ☃️Classic Christmas Songs 0x7f3497f60750>, 
	<Class Video VID=jiV7hyX65BM PROXY=None ID=3 NAME=ABBA GOLD GREATEST HITS - ABBA FULL ALBUM PLAYLIST 0x7f3497f60e50>, 
	<Class Video VID=Q3YkR_Eyh-s PROXY=None ID=4 NAME=Best Christmas Songs Playlist 2020 - Top 10 Christmas Songs || Merry Christmas Music Of All Time 0x7f3497f74bd0>, 
	<Class Video VID=fmfy9-Z4ZLc PROXY=None ID=5 NAME=Best Songs Of ABBA Collection 2020 | ABBA Greatest Hits Full Album 0x7f3497f7ae50>, 
	<Class Video VID=-PJDukRSHis PROXY=None ID=6 NAME=ABBA Best Songs Collection 2020 | Greatest Hits New Playlist Of ABBA 0x7f3497f8b0d0>, 
	<Class Video VID=ptaok2DmN0Y PROXY=None ID=7 NAME=Christmas 2020 🎁 Christmas Songs 2020 - 2021 🎄 Nonstop Christmas Songs Medley 2020 - 2021 0x7f3497f8bad0>, 
	<Class Video VID=dLU23pGXNF8 PROXY=None ID=8 NAME=NEW ABBA Full Album Playlist  || The Very Best Song #ABBA GOLD 0x7f349470ea10>]
	>>> p.get_dict
	[<Class Video VID=C-p3HnovSbU PROXY=None ID=0 NAME=Top ABBA Songs Playlist   #ABBA Best Mix 0x7f34987cd2d0>, 
	<Class Video VID=u44-KMrI4Hk PROXY=None ID=1 NAME=Top 100 Traditional Christmas Songs Ever - Best Classic Christmas Songs 2021 Collection 0x7f34987cdcd0>, 
	<Class Video VID=KOICR55wlGY PROXY=None ID=2 NAME=Merry Christmas 2021 ☃️ Beautiful Traditional Christmas Songs Playlist ☃️Classic Christmas Songs 0x7f3497f60750>, 
	<Class Video VID=jiV7hyX65BM PROXY=None ID=3 NAME=ABBA GOLD GREATEST HITS - ABBA FULL ALBUM PLAYLIST 0x7f3497f60e50>, 
	<Class Video VID=Q3YkR_Eyh-s PROXY=None ID=4 NAME=Best Christmas Songs Playlist 2020 - Top 10 Christmas Songs || Merry Christmas Music Of All Time 0x7f3497f74bd0>, 
	<Class Video VID=fmfy9-Z4ZLc PROXY=None ID=5 NAME=Best Songs Of ABBA Collection 2020 | ABBA Greatest Hits Full Album 0x7f3497f7ae50>, 
	<Class Video VID=-PJDukRSHis PROXY=None ID=6 NAME=ABBA Best Songs Collection 2020 | Greatest Hits New Playlist Of ABBA 0x7f3497f8b0d0>, 
	<Class Video VID=ptaok2DmN0Y PROXY=None ID=7 NAME=Christmas 2020 🎁 Christmas Songs 2020 - 2021 🎄 Nonstop Christmas Songs Medley 2020 - 2021 0x7f3497f8bad0>, 
	<Class Video VID=dLU23pGXNF8 PROXY=None ID=8 NAME=NEW ABBA Full Album Playlist  || The Very Best Song #ABBA GOLD 0x7f349470ea10>]


``p.downloadall(HIGH)`` will download full playlist in ``HIGH`` quality


Class Search
------------

.. code-block:: python

	>>> from youtube import Search
	>>> s = Search("taylor swift - willow")
	>>> s.videos
	[{'vid': 'RsEZmictANA', 'name': 'taylor swift - willow (official music video)'}, {'vid': '7EvwIw4gIyk', 'name': 'Taylor Swift - willow (Official Lyric Video)'}, {'vid': 'zI4DS5GmQWE', 'name': 'Taylor Swift - dorothea (Official Lyric Video)'}, {'vid': 'hP6QpMeSG6s', 'name': 'Taylor Swift - marjorie (Official Lyric Video)'}, {'vid': 'wDw8RCwmcKg', 'name': 'Taylor Swift - Willow (Lyrics)'}, {'vid': 'IEPomqor2A8', 'name': 'Taylor Swift - no body, no crime (Official Lyric Video) ft. HAIM'}, {'vid': '-qQogoNwJdM', 'name': "New TAYLOR SWIFT?! 'Willow' - My First Watch/Reaction!"}, {'vid': 'Oi2Vw0n2EfM', 'name': 'Taylor Swift - willow | Video Explained (Analysis, Easter eggs And More)'}, {'vid': 'OEd32AL-exA', 'name': 'Taylor Swift - Willow - Guitar Lesson'}, {'vid': 'jepo9tm22ig', 'name': 'Taylor Swift - Willow Cover'}, {'vid': 'qPOw4p36OLc', 'name': 'Taylor Swift - willow | Piano Cover by Pianella Piano'}, {'vid': '2TgkjFVqdJ0', 'name': 'Taylor Swift - willow - Music Video - REACTION'}, {'vid': 'ThOVwAmmLOo', 'name': 'Taylor Swift - Willow (Lyrics)'}, {'vid': 'NLIacgCnwFA', 'name': 'Taylor Swift - Willow - Reaction/Review'}, {'vid': '7B_DjCNKgHU', 'name': 'Taylor Swift - willow (Lyrics)'}, {'vid': 'O6IayU4FPmI', 'name': "Vocal Coach Reacts to Taylor Swift 'Willow' Evermore"}, {'vid': 'ufozmQSSY7c', 'name': 'Taylor Swift - Willow Reaction'}, {'vid': '1PKgktWMzNY', 'name': 'Taylor Swift - willow | Piano Tutorial'}, {'vid': '0ldUWIRURuw', 'name': 'taylor swift - willow - Piano Karaoke Instrumental Cover with Lyrics'}, {'vid': 'SqX8vbkG5_Q', 'name': 'Taylor Swift - willow (Piano Tutorial Easy)'}]
	>>> s.first
	<Class Video VID=RsEZmictANA PROXY=None ID=1 NAME=taylor swift - willow (official music video) 0x7f15a34c5a90>
	>>> 





How to get all title from playlist videos
------------------------------------------

A sample code to get all titles of playlist videos

.. code-block:: python

	from youtube import PlayList

	video_url = "https://www.youtube.com/playlist?list=PLeXILI4F6_4XJau4ZlJXD7-K75g6rDebr"

	p = PlayList(video_url)

	for n in p.get_dict: # This will return the raw dict with vid and name since we didnt used process=True
		print(n.get("name")) # This will print the title name


How to get description from all playlist video
-----------------------------------------------

A sample code to get description from all playlist video

.. code-block:: python

	from youtube import PlayList

	video_url = "https://www.youtube.com/playlist?list=PLeXILI4F6_4XJau4ZlJXD7-K75g6rDebr"

	p = PlayList(video_url, process=True)

	for n in p.get_dict: # This will return the Video class object since we used process=True
		print(n.description,end="\n\n") # This will print the description


How to get videos search query
-------------------------------

Sample code to get videos by search

.. code-block:: python

	from youtube import Search

	r = Search("taylor swift - willow")

	print(r.get_dict)
