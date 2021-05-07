## code pulled to create seperate file that can look through local cache
    #and call the scraper if needed



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
