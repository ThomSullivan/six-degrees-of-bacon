def process_second_degree(person):
    movies = list_movies(person[0])
    for movie in movies:

        current_cast = list_cast(movie)
        current_credits = []
        for credit in current_cast:
            tup = (credit[2], person[1], person[0], credit[1])
            current_credits.append(tup)
            #print(tup)
            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(process_cast, current_credits)
            conn1.commit()

def process_cast(credit):
    #print(credit)

        #print('Already Exists')
        return
    else:
        #print('made it')
        print(credit)
        
