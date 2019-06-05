from bs4 import BeautifulSoup
import urllib.request
import re
import queue


links_to_be_parsed = queue.Queue(maxsize=21000)
links_to_be_parsed.put("https://en.wikipedia.org/wiki/Web_scraping")

links_count = 0
links_file = open("links.txt",'a')
while links_to_be_parsed.qsize() > 0 and links_count <= 20000:
	dequeued_link = links_to_be_parsed.get()
	try:
		htmlpage = urllib.request.urlopen(dequeued_link)
		soup = BeautifulSoup(htmlpage)
		for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):							
			links_file.write(link.get('href'))
			links_file.write("\n")
			links_to_be_parsed.put(link.get('href'))
			links_count = links_count + 1
			print(links_count)
	except:
		print("Links: ",link)
		print(links_to_be_parsed.qsize())
links_file.close()
