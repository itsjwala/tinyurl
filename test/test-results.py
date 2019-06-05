import sys

sys.path.append("..")

from shortner import *


shorturl_file = open('links-short.txt',encoding = 'utf-8')
largeurl_file = open('links.txt',encoding = 'utf-8')

for shorturl,og_url in zip(shorturl_file.readlines(),largeurl_file.readlines()):
	shorturl = shorturl.strip('\r\n')
	og_url = og_url.strip('\r\n')

	if shorturl =="" or og_url == "":
		continue
	url = elate(shorturl)

	if url !=og_url:
		print(f"{og_url} <=> {shorturl} <=> {url}")





