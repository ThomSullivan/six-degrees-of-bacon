import sqlite3
import json
import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3
import time
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
conn1 = sqlite3.connect('../data/routes.db')
cur1 = conn1.cursor()

api_key = ''#'<put TMdb API key here>'

def unpack_IDS(list):
    new_list = [x[0] for x in list]
    return new_list

def json_request(address):
    '''Returns a JSON object from the supplied URL'''
    uh = urllib.request.urlopen(address, context=ctx)
    data = uh.read().decode()
    js = json.loads(data)
    return js

def query_details(type, id):
    address = 'https://api.themoviedb.org/3/{}/{}?api_key={}'.format(type, id, api_key)
    #print(address)
    return json_request(address)

def search_api(type, search):
    search = urllib.parse.quote_plus(search)
    address = 'https://api.themoviedb.org/3/search/{}?api_key={}&query={}'.format(type, api_key, search)
    #print(address)
    return json_request(address)

def get_person_name(person):
    '''Returns a string of the person's name with correct casing'''
    result = query_details('person', person)
    name = result['name']
    return name

def get_movie_title(movie):
    '''Returns movie title'''
    js = query_details('movie', movie)
    movie_title = js['title']
    return movie_title

def get_person_id(person):
    '''Returns the person's ID (passing in a name)'''
    result = search_api('person', person)
    person_id = result['results'][0]['id']
    person_name = result['results'][0]['name']
    return (person_id, person_name)

def construct_statement(list):
    '''contructs SQL statment based on the tabled the target was found in'''
    #print(list[-1])
    statement = 'SELECT * FROM '+ list[-1]
    part_one = ' JOIN '
    part_two = []
    part_three = ' WHERE '+list[-1]+'.ID = ?;'
    if len(list) <=1:
        statement = ( '''SELECT * FROM first_degree WHERE ID = ?''')
        return statement
    new_list = list.copy()
    new_list.pop()
    part_one = part_one + ', '.join(new_list)
    statement = statement + part_one + ' ON '
    list_counter = 1
    for item in list:
        #print(list[(list_counter+1)])
        if list_counter >= len(list):
            break
        else:
            string = item +'.ID=' +list[list_counter]+'.previous'
            part_two.append(string)
            list_counter += 1
    next_string = ' AND '.join(part_two)
    statement = statement + next_string + part_three

    return statement
#print(target)
tables = ['first_degree','second_degree','third_degree','fourth_degree','fifth_degree']
degrees = {}
#create an index to locate target in database
for table in tables:
    cur1.execute('''SELECT ID FROM '''+table)
    degrees[table] = unpack_IDS(cur1.fetchall())

#get input of name to show connection for
#find id IF in database
while True:
    target_name = ''
    entry_degree = ''
    target = input('Who do you want to connect to Kevin Bacon? ')
    if len(target) < 1:
        break
    try:
        target = get_person_id(target)
    except:
        print('error not found')
        continue
    target_name = target[1]
    target = target[0]

    for degree, people in degrees.items():
        if target in people:
            entry_degree = degree
    print(target_name, 'connected in the ', entry_degree)
    try:
        this_list = tables[:(tables.index(entry_degree)+1)]
    except:
        print("not available add more degrees")
        continue
    statement = construct_statement(this_list)
    cur1.execute(statement,(target,))
    route = cur1.fetchall()
    route = route[0]
    #this has to be done due to data structures within the data base ID is route[1] for first_degree
    # but route[2] is used for the rest
    if len(this_list) == 1:
        output = target_name+' was in '+ get_movie_title(route[1]) + ' with Kevin Bacon'
        print(output)
    elif len(this_list) == 2:
        output = target_name + ' was in ' + get_movie_title(route[2])  +' with\n' + get_person_name(route[3]) +' who was in ' + get_movie_title(route[4]) + ' \nwith Kevin Bacon'
        print(output)
    else:
        first_part = target_name + ' was in ' + get_movie_title(route[2])  +' with\n'
        final_part = ' who was in ' + get_movie_title(route[4]) + ' with\n'
        middle_part = ''
        tuple_couter = 0
        string = ''
        string1 = ''
        for item in route[5:]:
            if tuple_couter == 0:
                string = get_person_name(item) + ' who was in '
                tuple_couter += 1
            elif tuple_couter == 1:
                string1 = get_person_name(item) + ' who was in '
                tuple_couter +=1
            else:
                middle_part = middle_part + string + get_movie_title(item) + ' with\n' + string1
                string = ''
                string1 = ''
                tuple_couter = 0
        output = first_part + middle_part + final_part + 'Kevin Bacon!'
        print(output)
#pull route data w/ FKs
#use route data to make API requests
    #data needed is (name,Movie,year) for each degree maybepacked into a dictionary?
    #{first_degree:(name,movie,year)}
#print out contents of dictionary
