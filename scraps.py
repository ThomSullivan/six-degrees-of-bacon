def query_get(type, id, get_type):
    address = 'https://api.themoviedb.org/3/{}/{}/{}?api_key={}'.format(type, id, get_type, api_key)
    #print(address)
    return json_request(address)

def search_api(type, search):
    search = urllib.parse.quote_plus(search)
    address = 'https://api.themoviedb.org/3/search/{}?api_key={}&query={}'.format(type, api_key, search)
    #print(address)
    return json_request(address)

def query_get(type, id, get_type):
    address = 'https://api.themoviedb.org/3/{}/{}/{}?api_key={}'.format(type, id, get_type, api_key)
    #print(address)
    return json_request(address)

def query_details(type, id):
    address = 'https://api.themoviedb.org/3/{}/{}?api_key={}'.format(type, id, api_key)
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
def get_movie_title(movie):
    '''Returns movie ID'''
    js = search_api('movie', movie)
    movie_title = js['results'][0]['title']
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
