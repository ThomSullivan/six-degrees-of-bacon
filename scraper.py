import json
import urllib.request, urllib.parse, urllib.error
#import xml.etree.ElementTree as ET
import ssl
import sqlite3
import time
import sys
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#constant data
conn = sqlite3.connect('../data/bacon_DB1.db')
cur = conn.cursor()
count = 0
api_key = ''#'<put TMdb API key here>'

def json_request(address):
    '''Returns a JSON object from the supplied URL'''
    uh = urllib.request.urlopen(address, context=ctx)
    data = uh.read().decode()
    js = json.loads(data)
    return js

def query_get(type, id, get_type):
    address = 'https://api.themoviedb.org/3/{}/{}/{}?api_key={}'.format(type, id, get_type, api_key)
    #print(address)
    return json_request(address)

cur.execute('''CREATE TABLE IF NOT EXISTS "credits" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"movie_id"	INTEGER NOT NULL,
	"person_id"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
    );''')
amount = input('Pull how many movie credit lists?')
amount = int(amount)
cur.execute('''SELECT * FROM credits ORDER BY movie_id DESC LIMIT 1''')
try:
    id = cur.fetchone()[1]
except:
    id = 0
id += 1

while count < int(amount):
    try:
        data = query_get('movie', id, 'credits')
    except:
        id += 1
        continue
    #some ids are invalid
    if len(data['cast']) == 0:
        id = id + 1
        continue
    if data['cast'][0]['adult'] == 'true':
        id += 1
        continue

    count = count + 1
    print((count/amount)*100)
    id = id + 1

    for entry in data['cast']:
        #print('movie ID:', data['id'], ' person name: ', entry['name'])
        cur.execute('''INSERT INTO credits (movie_id, person_id)
            VALUES ( ?, ? )''', (data['id'], entry['id']))
    conn.commit()
