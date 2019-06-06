import sqlite3
import os


PATH = "C:\\Users\\jigar\\Desktop\\shortner\\tinyurls.db"

def create_db():
	con = sqlite3.connect(PATH)
	query = """	
	create table if not exists mappings(id integer PRIMARY KEY AUTOINCREMENT,
	url varchar, shorturl varchar)
	"""
	con.execute(query)
	con.commit()
	con.close()

def insert_entry(url,shorturl):
	con = sqlite3.connect(PATH)
	query = """
	insert into mappings(url,shorturl) values(?,?)
	"""
	con.execute(query,(url,shorturl))
	con.commit()
	con.close()

def cleanup():
	con = sqlite3.connect(PATH)

	query = """
	delete from mappings;"""
	con.execute(query)
	query = "delete from sqlite_sequence where name='mappings';"
	con.execute(query)
	con.commit()
	con.close()


charmaps = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
n = len(charmaps)

def shorten(url):

	con = sqlite3.connect(PATH)
	cur = con.cursor()
	cur.execute("select count(*) from mappings")
	
	id = cur.fetchone()[0]
	if id is None:
		id = 1
	else:
		id += 1
	
	shorturl = ""
	
	while id>0:
		# only seven characters so ignoring performance loss due to immutability

		shorturl += charmaps[id%n]
		id//=n;

	shorturl = shorturl[::-1]
	shorturl = f"jig.lu/{shorturl}"
	insert_entry(url,shorturl)

	return shorturl


def elate(shorturl):
	# jig.lu/GHhh90

	shorturl = shorturl[7:]
	id = 0
	

	for i in shorturl:
		ascii = ord(i)
		
		if ascii >= ord('A') and ascii <= ord('Z'):
			idx = ascii - ord('A')
		elif ascii >= ord('a') and ascii <= ord('z'):
			idx = ascii - ord('a') + 26
		elif ascii >= ord('0') and ascii <= ord('9'):
			idx = ascii - ord('0') +26 + 26
		else :
			raise Error('oopsie')
		
		id  = id*n + idx
		
		

	# print(id)
	con = sqlite3.connect(PATH)
	cur = con.cursor()

	cur.execute("select * from mappings where id = ?",(id,))

	url = cur.fetchone()
	if url is None:
		print(f"yeh none \n {shorturl} {id}")
	con.close()
	return url[1]


if not os.path.exists(PATH):
	create_db()
