#!/usr/bin/python3
import sys
sys.path.insert(0,'..')

import beta as youtube
from beta import Search

r = Search("a kermit song")

print(r.get_dict)


if __name__ == '__main__':
	print(youtube.__version__)