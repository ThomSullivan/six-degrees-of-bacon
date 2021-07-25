import concurrent.futures
import sqlite3
conn = sqlite3.connect('bacon_DB.db')
cur = conn.cursor()
conn1 = sqlite3.connect('routes.db')
cur1 = conn1.cursor()

def list_movies(person):
    '''Returns a list of movie IDs for the person ID passed in'''
    cur.execute('''SELECT DISTINCT movie_id
                    FROM credits
                    WHERE person_id = ?''', (person,))

    movies = [item[0] for item in cur.fetchall()]
    return movies

def list_cast(movie):
    cur.execute('''SELECT * FROM credits WHERE movie_id = ?''', (movie,))
    current_movie = cur.fetchall()
    return current_movie

def unpack_IDS(list):
    new_list = [x[0] for x in list]
    return new_list

def process_second_degree(info):
    '''Pass in a tuple of info about first degree route(movie,person)'''
    #print(person)
    existing_movies.append(info[0])
    current_cast = list_cast(info[0])
    for credit in current_cast:
        if credit[2] in existing_routes or credit[2] == BaconID:
            #print('Already Exists') #Debugger
            continue
        else:
            #print(credit[2]) #Debugger
            cur1.execute('''INSERT OR IGNORE INTO second_degree (ID, previous, movie)
            VALUES ( ?, ?, ?)''', (credit[2], info[1], credit[1],))
            existing_routes.append(credit[2])
    conn1.commit()

BaconID = 4724
#get the list of tuples for use
cur1.execute('''SELECT * FROM first_degree''')
previous_degree = cur1.fetchall()
#get the list of existing routes for checks
cur1.execute('''SELECT ID FROM first_degree''')
existing_routes = unpack_IDS(cur1.fetchall())
cur1.execute('''SELECT ID FROM second_degree''')
existing_routes = existing_routes + unpack_IDS(cur1.fetchall())
existing_routes.append(BaconID)
#create a list of movies in the DB for checks
cur1.execute('''SELECT movie FROM first_degree''')
existing_movies = unpack_IDS(cur1.fetchall())
cur1.execute('''SELECT movie FROM second_degree''')
existing_movies = existing_movies + unpack_IDS(cur1.fetchall())
#process_second_degree(first_degree[1]) #<-- debugger
if __name__ == '__main__':
    print('hello')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for person in previous_degree:

            person = person[0]
            movies = list_movies(person)
            tup = [(movie, person) for movie in movies if movie not in existing_movies]
            #process_second_degree(tup[0])
            executor.map(process_second_degree, tup)
