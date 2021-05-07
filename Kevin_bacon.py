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

#other methods
def detect_bacon(lst):
    '''Returns a list of intersections of list with bacon_list'''
    lst3 = [value for value in lst if value in bacon_list]
    if len(lst3) > 0:
        return (True, lst3)
    else:
        return False


#constant data
# a list of movies Kevin Bacon is in to start comparisons
bacon_list = ['Apollo 13', 'Footloose', 'Top Gun']#fill this list!


while True:
    person = input("Enter a person's name: ")
    if len(person) == 0:
        break
    db_name = get_actor_name(person)
    print(db_name)
    #first compare top 10 movies to bacon bacon_list
    degree_zero = top_movies(10, person)
    print(degree_zero)
    if detect_bacon(degree_zero) == True:
        print('Found some bacon!')
        break
    #print(check)
#If nothing found compile list of top ten actors from top ten movies
    degree_one_actors = []
    for movie in degree_zero:
        next_list = top_cast(10, movie)
        for name in next_list:
            if name == db_name:
                continue
            elif name not in degree_one_actors:
                degree_one_actors.append(name)
    #print(degree_one_actors)
    degree_one_movies = []

    for person in degree_one_actors:
        try:
            for movie in top_movies(10, person):
                if movie in degree_one_movies:
                    continue
                elif movie in degree_zero:
                    continue
                else:
                    degree_one_movies.append(movie)
        except:
            continue





# now detect_bacon on top ten movies of each person on degree_one
# keep a list, maybe a dictionary would work to store the degree lists
# {one_movies: [], one_actors:[], two_movies[], two_actors[], ....}
#    degree_one_actors = []
#    for actor in degree_one:
    #    actor = actor.replace(' ', '+')

#        print(top_ten_movies(actor))
