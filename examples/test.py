#!/usr/bin/python3
import sys
sys.path.insert(0,'..')

import youtube as youtube
from youtube import Search, Video

streams = Video("https://www.youtube.com/watch?v=B6_iQvaIjXw").streams
for n in streams:
	print(n)
	print(n.url)
	print("\n\n")
print(streams.ffresolution(720).av)

# y = youtube.Video("https://www.youtube.com/watch?v=5sFDOiGyAG8")
# print(y)

if __name__ == '__main__':
	print(youtube.__version__)