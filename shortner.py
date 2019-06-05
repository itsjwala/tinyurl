import sqlite3
import os

def create_db():
	con = sqlite3.connect('tinyurls.db')
	query = """	
	create table if not exists mappings(id integer PRIMARY KEY AUTOINCREMENT,
	url varchar, shorturl varchar)
	"""
	con.execute(query)
	con.commit()
	con.close()

def insert_entry(url,shorturl):
	con = sqlite3.connect('tinyurls.db')
	query = """
	insert into mappings(url,shorturl) values(?,?)
	"""
	con.execute(query,(url,shorturl))
	con.commit()
	con.close()



charmaps = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
n = len(charmaps)


def shorten(url):

	con = sqlite3.connect('tinyurls.db')
	cur = con.cursor()
	cur.execute("select count(*) from mappings")
	
	id = cur.fetchone()[0]
	if id is None:
		id = 1
	else:
		id+=1
	
	shorturl = ""
	
	while id>0:
		# only seven characters so ignoring performance loss due to immutability

		shorturl += charmaps[id%n]
		id//=n;

	shorturl = shorturl[::-1]

	insert_entry(url,shorturl)

	return f"jig.lu/{shorturl}"


def elate(shorturl):
	# jig.lu/GHhh90

	shorturl = shorturl[7:]
	id = 0
	count = 0
	for i in shorturl:
		ascii = ord(i)
		
		if ascii >= ord('A') and ascii <= ord('Z'):
			idx = ascii - ord('A')
		elif ascii >= ord('a') and ascii <= ord('z'):
			idx = ascii - ord('A') + 26
		else:
			idx = ascii - ord('0') +26 + 26

		
		id += 62**count * idx
		count +=1

	# print(id)
	con = sqlite3.connect('tinyurls.db')
	cur = con.cursor()

	cur.execute("select * from mappings where id = ?",(id,))

	print(cur.fetchall())

	con.close()


if not os.path.exists("tinyurls.db"):
	create_db()

