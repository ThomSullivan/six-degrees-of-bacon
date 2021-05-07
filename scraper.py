import json
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#constant data


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

#actor methods
def get_actor_id(actor):
    '''Returns the actor's ID'''
    result = search_api('person', actor)
    actor_id = result['results'][0]['id']
    return actor_id

def get_actor_name(actor):
    '''Returns a string of the actor's name with correct casing'''
    id = get_actor_id(actor)
    result = query_details('person', id)
    name = result['name']
    return name

def top_movies(n, actor):
    '''Returns a list of the first n movie credits of an actor'''
    lst = []
    actor_id = get_actor_id(actor)
    movies = query_get('person', actor_id, 'movie_credits')
    for i in range(n):
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

def top_cast(n, movie):
    '''Returns a list of the first n billed actors'''
    lst = []
    cast = get_movie_credits(movie)
    for person in cast['cast'][:n]:
        lst.append(person['name'])
    return lst

# this part of code is mostly just for output use
while True:
    person = input("Enter a person's name: ")
    if len(person) == 0:
        break
