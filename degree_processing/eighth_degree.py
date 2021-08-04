import concurrent.futures
import sqlite3
conn = sqlite3.connect('../data/bacon_DB.db')
cur = conn.cursor()
conn1 = sqlite3.connect('../data/routes.db')
cur1 = conn1.cursor()

def list_movies(person):
    '''Returns a list of movie IDs for the person ID passed in'''
    cur.execute('''SELECT DISTINCT movie_id
                    FROM credits
                    WHERE person_id = ?''', (person,))

    movies = [item[0] for item in cur.fetchall()]
    return movies

def unpack_IDS(list):
    new_list = [x[0] for x in list]
    return new_list

def list_cast(movie):
    cur.execute('''SELECT * FROM credits WHERE movie_id = ?''', (movie,))
    current_movie = cur.fetchall()
    return current_movie

def process_eighth_degree(info):
    '''Pass in a tuple of info about seventh degree route(movie,person)'''
    #print(person)
    existing_movies.append(info[0])
    current_cast = list_cast(info[0])
    for credit in current_cast:
        if credit[2] in existing_routes:
            #print('Already Exists') #Debugger
            continue
        else:
            #print(credit[2]) #Debugger
            cur1.execute('''INSERT OR IGNORE INTO eighth_degree (ID, previous, movie)
            VALUES ( ?, ?, ?)''', (credit[2], info[1], credit[1],))
            existing_routes.append(credit[2])
    conn1.commit()
BaconID = 4724
counter = 1
cur1.execute('''CREATE TABLE IF NOT EXISTS "eighth_degree" (
	"ID"	INTEGER UNIQUE,
	"previous"	INTEGER,
	"movie"	INTEGER,
	PRIMARY KEY("ID"),
	FOREIGN KEY("previous") REFERENCES "seventh_degree"("ID")
);''')
#get the list of tuples for use
cur1.execute('''SELECT ID FROM seventh_degree''')
previous_degree = unpack_IDS(cur1.fetchall())
tables = ['first_degree','second_degree','third_degree','fourth_degree','fifth_degree','sixth_degree',
            'seventh_degree','eighth_degree']
existing_routes = []
existing_movies = []
for table in tables:
    #create a list of movies,and people in the DB for checks
    cur1.execute('''SELECT ID FROM '''+table)
    existing_routes = existing_routes + unpack_IDS(cur1.fetchall())
    cur1.execute('''SELECT DISTINCT movie FROM '''+table)
    existing_movies = existing_movies + unpack_IDS(cur1.fetchall())

#get the list of existing routes for checks
existing_routes.append(BaconID)
#print(len(existing_movies))
#process_second_degree(first_degree[1]) #<-- debugger
total = len(previous_degree)
counter = 1
if __name__ == '__main__':
    print('hello')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for person in previous_degree:
            print(counter/total)
            counter += 1
            movies = list_movies(person)
            #tuples are the only way I could get these next steps to run concurrently and retain the person ID
            #for the previous field in the database
            tup = [(movie, person) for movie in movies if movie not in existing_movies]
            #print(len(tup))
            #process_third_degree(tup[0])
            executor.map(process_eighth_degree, tup)
