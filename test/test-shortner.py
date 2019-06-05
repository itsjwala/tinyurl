import sys

sys.path.append("..")

from shortner import *

import os

short_link_file = open('links-short.txt','w')

count = 0
cleanup()
with open("links.txt",encoding="utf8") as f:
	for line in f.readlines():
		if count == 200:
			break

		line = line.strip("\r\n")
		if line == "":
			continue
		shorturl = shorten(line)
		print(line,end = " ")
		print(shorturl)
		short_link_file.write(shorturl)
		short_link_file.write(os.linesep)
		count+=1

short_link_file.close()

