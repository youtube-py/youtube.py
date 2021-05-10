import sys

if __name__ == '__main__':
	sys.path.insert(0,'..')

import logging
import argparse
import re
from youtube import Video, PlayList, __version__, __github__

class main:
	'''
	This is main cli class for youtube.py
	'''
	def __init__(self):
		self.args = self.process_args()

		self.url = self.check_url(self.args.url)

		self.conn = self.args.connections

		if "playlist" in self.url:
			self.PlayList = True
			self.videos = [f"https://youtu.be/{n['vid']}" for n in PlayList(self.url).get_dict]
		else:
			self.PlayList = False
			self.videos = list([self.url])

		if self.args.output:
			self.output = self.args.output
		else:
			self.output = ""

		if self.args.logs:
			self.process_logg()

		if self.args.streams:
			self.print_streams()

		if self.args.ffmpeg:
			self.process_ffmpeg()

		if self.args.video:
			self.process_video()
		
		if self.args.itag:
			self.process_itag()

		if self.args.audio:
			self.process_audio()

		if self.args.resolution:
			self.process_resolution()
		exit()

	def print_streams(self):
		if self.args.streams:
			for n in self.videos:
				print(f'Video url: {n}')
				for m in Video(n).streams:
					print(m)

	def check_url(self, url:str) -> str:
		'''
		This will check the url type
		'''
		match = [re.compile(r'(http|https)://youtu.be/(.+)'),
				re.compile(r'(http|https)://(www.)?youtube.com/watch\?v=(.+)'),
				re.compile(r'(http|https)://(www.)?youtube.com/playlist\?list=(.+)'),]
		for n in match:
			if n.match(url):
				return url


	def process_ffmpeg(self):
		quality = self.parse_quality(self.args.ffmpeg)
		for n in self.videos:
			if self.PlayList:
				print(f'Downloading: {n}')

			if quality == 0:
				name = Video(n).streams.ffhigh.download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")

			elif quality == 1:
				name = Video(n).streams.ffmid.download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")
			
			else:
				name = Video(n).streams.fflow.download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")


	def process_video(self):
		quality = self.parse_quality(self.args.video)
		for n in self.videos:
			if self.PlayList:
				print(f'Downloading: {n}')

			if quality == 0:
				name = Video(n).streams.get_both.high().download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")

			elif quality == 1:
				name = Video(n).streams.get_both.mid().download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")
			
			else:
				name = Video(n).streams.get_both.low().download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")


	def process_audio(self):
		quality = self.parse_quality(self.args.audio)
		for n in self.videos:
			if self.PlayList:
				print(f'Downloading: {n}')

			if quality == 0:
				name = Video(n).streams.get_audios.high().download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")

			elif quality == 1:
				name = Video(n).streams.get_audios.mid().download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")
			
			else:
				name = Video(n).streams.get_audios.low().download(dire=self.output, status=True, connection=self.conn)
				if name:
					print(f"{name} Downloaded")


	def process_resolution(self):
		resolution = self.args.resolution
		for n in self.videos:
			if self.PlayList:
				print(f'Downloading: {n}')

			streams = Video(n).streams
			name = streams.ffresolution(resolution).download(dire=self.output, status=True, connection=self.conn)
			if name:
				print(f"{name} Downloaded")


	def process_itag(self):
		itag = self.args.itag
		for n in self.videos:
			if self.PlayList:
				print(f'Downloading: {n}')

			name = Video(n).streams.get_itag(itag).download(dire=self.output, status=True, connection=self.conn)
			if name:
				print(f"{name} Downloaded")


	def parse_quality(self,q:str) -> int:
		if q.lower() == "high":
			return 0
		elif q.lower() == "mid":
			return 1
		else:
			return 2


	def process_logg(self):
		logging.basicConfig(level=logging.DEBUG,
			format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s")


	def process_args(self):
		parser = argparse.ArgumentParser(description="Definitions:\n  Quality Types: ('HIGH','MID', 'LOW')\n"
			"  Video resolution examples. ('144', '240', '360', '480', '720', '1080') more/less depend on your video\n"
			"\nNote:\n  Default values for '--ffmpeg', '--video', '--audio' is 'HIGH'\n"
			"  Default values for '--resolution' is 720",
											formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('url', help='Enter video or playlist url')
		parser.add_argument('-o', '--output', type=str, help='Output location for downloading streams.')
		parser.add_argument('-l', '--logs', action='store_true', help='To enable extra logs.')
		parser.add_argument('-c', '--connections', const=8, nargs="?", default=8, type=int, help='Number of connections in download.')
		parser.add_argument('--version', action="version", version=f'Youtube.py version {__version__} ({__github__})',help='Check the current version of youtube.py')
		
		group = parser.add_mutually_exclusive_group(required=True)

		group.add_argument('-ff', '--ffmpeg', const="HIGH", nargs="?", type=str, help='FFMPEG downloads audio/video both then copy in one file, Pass the quality type.')
		group.add_argument('-v', '--video', const="HIGH", nargs="?", type=str, help='Downlaod video (only progressive), Pass quality.')
		group.add_argument('-i', '--itag', type=int, help='Download stream with itag, Pass itag id.')
		group.add_argument('-s', '--streams', action='store_true', help='This argument will list the all available streams.')
		group.add_argument('-a', '--audio', const="HIGH", nargs="?", type=str, help='Download audio, Pass quality.')
		group.add_argument('-r', '--resolution', const=720, nargs="?", type=int, help='Download stream with quality type, Pass video resolution.')
		args = parser.parse_args()
		return args


if __name__ == '__main__':
	main()