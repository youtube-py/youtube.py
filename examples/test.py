#!/usr/bin/python3
import sys
sys.path.insert(0,'..')

import youtube as youtube
from youtube import Search

r = Search("a kermit song")

print(r.get_dict)

y = youtube.Video("https://www.youtube.com/watch?v=5sFDOiGyAG8")
print(y)

if __name__ == '__main__':
	print(youtube.__version__)