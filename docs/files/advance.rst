.. _advance:

Advance Codes
==============

How to download mass videos with ffmpeg.
----------------------------------------

.. code-block:: python

	from youtube import Video

	video_url = ["3AtDnEC4zak", "3AtDnEC4zak"]

	for vdo in video_url:
		v = Video(f"https://youtu.be/{vdo}").streams
		v.ffhigh.download() # ffhigh will download stream with highest quality

For download low and mid quality use ``ffmid`` and ``fflow`` 

Use ``status=True`` in download to show process bar

How to download mass videos with ffmpeg and resolutions.
---------------------------------------------------------


.. code-block:: python

	from youtube import Video

	video_url = ["3AtDnEC4zak", "3AtDnEC4zak"]

	for vdo in video_url:
		v = Video(f"https://youtu.be/{vdo}").streams
		v.ffresolution(quality=480).download() # ffresolution will return the FFMPEG class

``480`` is stream quality/resolution.



How to download all playlist videos concurrently/fast.
-------------------------------------------------------

.. code-block:: python

	from youtube import PlayList

	video_url = "https://www.youtube.com/playlist?list=PLeXILI4F6_4XJau4ZlJXD7-K75g6rDebr"

	p = PlayList(video_url, process=True) # process=True to generate all Video objects

	for n in p.get_object:
		print(n) # n is the Video object


``p.get_object`` will return the list of :class:`Video <Video>`

now we will use :class:`concurrent.futures <concurrent.futures>` for concurrently download


.. code-block:: python

	from youtube import PlayList
	import concurrent.futures


	MAX_CONCURRENT_DOWNLOADS = 1 #max concurrent download at ones

	video_url = "https://www.youtube.com/playlist?list=PLeXILI4F6_4XJau4ZlJXD7-K75g6rDebr"

	p = PlayList(video_url, process=True) # process=True to generate all Video objects

	func = lambda x: x.streams.get_audios.low().download()

	with  concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
		for n in executor.map(func,p.get_object):
			print(f'{n} Downloaded')

.. note::
	
	Becareful when using concurrent set ``MAX_CONCURRENT_DOWNLOADS`` according to your internet speed
	connection will get close after ``5`` second if no data ``recv``


Other examples
---------------


.. code-block:: python

	from youtube import Video

	video_url = ["3AtDnEC4zak", "3AtDnEC4zak"]

	for vdo in video_url:
		v = Video(f"https://youtu.be/{vdo}").streams
		v.get_both.high()

``get_both`` will return the streams with audio/video both and high will return the first stream from the list
example ``return self.data[0]`` like  ``get_both.high()`` or ``get_both[0]`` are the same.

``high()`` will return the first stream so ofcause it will a :class:`Stream <Stream>`

with ``.url`` you can even call the stream url of that perticular stream ie. ``v.get_both.high().url``


.. code-block:: python

	from youtube import Video

	video_url = ["3AtDnEC4zak", "3AtDnEC4zak"]

	for vdo in video_url:
		v = Video(f"https://youtu.be/{vdo}").streams
		url = v.get_both.high().url
		print(url)