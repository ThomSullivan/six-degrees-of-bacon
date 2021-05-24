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
conn = sqlite3.connect('bacon_DB.db')
cur = conn.cursor()
count = 0
id = 1

def json_request(address):
    '''Returns a JSON object from the supplied URL'''
    uh = urllib.request.urlopen(address, context=ctx)
    data = uh.read().decode()
    js = json.loads(data)
    return js

def search_api(type, search):
    search = urllib.parse.quote_plus(search)
    address = 'https://api.themoviedb.org/3/search/{}?api_key=f9abc524c812cc4b2476a9cda95bddf7&query={}'.format(type, search)
    #print(address)
    return json_request(address)

def query_get(type, id, get_type):
    address = 'https://api.themoviedb.org/3/{}/{}/{}?api_key=f9abc524c812cc4b2476a9cda95bddf7'.format(type, id, get_type)
    #print(address)
    return json_request(address)

def query_details(type, id):
    address = 'https://api.themoviedb.org/3/{}/{}?api_key=f9abc524c812cc4b2476a9cda95bddf7'.format(type, id)
    #print(address)
    return json_request(address)

#person methods
def get_person_id(person):
    '''Returns the person's ID (passing in a name)'''
    result = search_api('person', person)
    person_id = result['results'][0]['id']
    return person_id

def get_person_name(person):
    '''Returns a string of the person's name with correct casing'''
    id = get_person_id(person)
    result = query_details('person', id)
    name = result['name']
    return name

def get_person_rating(person):
    '''Returns an persons popularity rating(passing in a name) '''
    id = get_person_id(person)
    result = query_details('person', id)
    name = result['popularity']
    return name

def get_movies(person):
    '''Returns a list of the movie credits of an person, slice to truncate'''
    lst = []
    person_id = get_person_id(person)
    movies = query_get('person', person_id, 'movie_credits')
    for i in range(len(movies['cast'])):
        lst.append(movies['cast'][i]['title'])
    return lst

#movie methods
def get_movie_id(movie):
    '''Returns movie ID'''
    js = search_api('movie', movie)
    movie_id = js['results'][0]['id']
    return movie_id

def get_movie_credits(movie):
    '''Returns a dictionary of the full credits of a movie requires INT for id'''
    id = get_movie_id(movie)
    cast_list = query_get('movie', id, 'credits')
    return cast_list

def get_cast(movie):
    '''Returns a list of billed persons, slice to truncate'''
    lst = []
    cast = get_movie_credits(movie)
    for person in cast['cast']:
        lst.append(person['name'])
    return lst

req_type = input('What type of request?(person, movie, cast)')
req_type = req_type.lower()

if req_type == "person":
    amount = input('person request: Pull how many records?')
    cur.execute('''SELECT * FROM person ORDER BY id DESC LIMIT 1''')
    id = cur.fetchone()[0] + 1
    fail_count = 0
    while count < int(amount):
#some ids are invalid
        try:
            data = query_details("person", id)
        except:
            fail_count = fail_count + 1
            id = id + 1
            continue
        count = count + 1
        print(data['name'],":  ID:", id)
        cur.execute('''INSERT INTO person (id, name, rating)
            VALUES ( ?, ?, ? )''', (id, data['name'], data['popularity']))
        id = id + 1
    conn.commit()
    print('Failed requests: ', fail_count)

elif req_type == "movie":
    amount = input('movie request: Pull how many records?')
    cur.execute('''SELECT * FROM movie ORDER BY id DESC LIMIT 1''')
    id = cur.fetchone()[0] + 1
    fail_count = 0
    while count < int(amount):
#some ids are invalid
        try:
            data = query_details("movie", id)
        except:
            fail_count = fail_count + 1
            id = id + 1
            continue
        count = count + 1
        print(data['title'],":  ID:", id)
        cur.execute('''INSERT INTO movie (id, title, rating)
            VALUES ( ?, ?, ? )''', (id, data['title'], data['vote_average']))
        id = id + 1
    conn.commit()
    print('Failed requests: ', fail_count)

elif req_type == 'cast':
    print('****WARNING each cast request adds many records to local DB*****')
    amount = input('cast request: Pull how many records?')
    cur.execute('''SELECT * FROM credits ORDER BY movie_id DESC LIMIT 1''')
    id = cur.fetchone()[1]
    print(id)
    fail_count = 0

    while count < int(amount):
        id = id + 1
#some ids are invalid
        try:
            data = query_get('movie', id, 'credits')
        except:
            fail_count = fail_count + 1
            continue
        count = count + 1

        for entry in data['cast']:
            print('movie ID:', data['id'], ' person name: ', entry['name'], ' Character: ', entry['character'])
            cur.execute('''INSERT INTO credits (movie_id, person_id, appearing_as)
                VALUES ( ?, ?, ? )''', (data['id'], entry['id'], entry['character']))
        for entry in data['crew']:
            cur.execute('''INSERT INTO credits (movie_id, person_id, appearing_as)
                VALUES ( ?, ?, ? )''', (data['id'], entry['id'], entry['job']))

    conn.commit()
    print('Failed requests: ', fail_count)

else:
    print('error')
