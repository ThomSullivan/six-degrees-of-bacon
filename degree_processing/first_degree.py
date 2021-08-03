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
                    WHERE person_id = ?;''', (person,))
    movies = [item[0] for item in cur.fetchall()]
    return movies

def list_cast(movie):
    cur.execute('''SELECT * FROM credits WHERE movie_id = ?''', (movie,))
    current_movie = cur.fetchall()
    return current_movie
#credit[2] is the person_id in the database
#credit[1] is the movie ID in the database

def process_first_degree(movie):
    current_cast = list_cast(movie)
    for credit in current_cast:
        if credit[2] == BaconID:
            #print('Already Exists')
            continue
        else:
            #print(credit[3])
            cur1.execute('''INSERT OR IGNORE INTO first_degree (ID, movie)
            VALUES ( ?, ?)''', (credit[2], movie,))
    conn1.commit()


if __name__ == '__main__':
    BaconID = 4724
    con1.execute('''CREATE TABLE IF NOT EXISTS "first_degree" (
    	"ID"	INTEGER UNIQUE,
    	"movie"	INTEGER,
    	PRIMARY KEY("ID")
    );''')
    print('hello')
    movies = list_movies(BaconID)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_first_degree, movies)
    print('good')
