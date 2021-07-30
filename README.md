# six-degrees-of-bacon
Kevin bacon suite
The source of all data used for this project:
https://www.themoviedb.org
Ask for a name to link to Kevin Bacon(KB)
search cache database for a route to KB
if not found
scrape TMDB movie API until route is found
add new route and results to cache database
update route table with any new routes found
remove any obsolete routes
^ old stuff but I want to keep it
----------------------------
This project has really taken off and after working on it for a while I think the route it is now on will work well. A high level view is this: Gather data to use to find connections, find all the connections, and serve that information out. The Movie database (TMdb) was used as the source, and information was retrieved through the REST API, using python and stored locally. The next step will be moving through the database to record all the connections to Kevin Bacon, this will all be recorded in a second database. Finally the plan is to use the Django framework to host this content as a web app.

Continued work on this project quickly revealed that using API requests to find connections to Kevin Bacon would probably upset the people running TMdb. So I have decided to collect all the relevant data and use API requests to fill in information in the final interface. This should keep the local database size down, only having on hand the appropriate ID numbers to fetch information from TMdb. A scraper was built to pull only as much data as needed for local storage and use in identifying connections to Kevin Bacon.

For collecting the needed data all person ID and movie ID numbers have been pulled, also credit lists for each movie will be needed to actually make the connections. This being written in retrospect some data that has been pulled that is not needed such as strings for names of movies, people, and credits. I did however make use of this extra data for ease of development, allowing me to see human readable names to think through all the steps. These names allowed me to catch something that I otherwise would have been unaware of until seeing the final outputs of the project. TMdb has "adult" films in it, a lot of them. Maybe I can make an 'after dark' section the internet loves these kinds of films :D. I will have to write a quick script to remove these to ensure family friendliness. The final database put together is about a 400mB file and includes 1,876,658 people, 587,054 movies, and a whopping 7,144,819 movie credits.

When the scraper was done pulling all the data needed. Work started on sifting through all these people and movies looking for connections to Kevin Bacon. My original thought was to have a single program that just went through and did not stop until all connections were made, this seemed to lead to issues if the program had to be restarted. The main issue being I have not yet figured out a good way to continue from the last commit. I thought that I could filter any IDs that were listed as a previous step, but this proved to be ineffective as the person the program stopped on would be incomplete, never to be finished. Because of this the script must start at the top of the list and work its way through the entire degree again. To remedy the situation I decided to split each degree into a separate script for use after the previous had been run.

The first script just writes data about people in Kevin Bacon movies, everyone. This is when I started to think maybe I will remove crew and include only people that have been credited with an on screen role. My fear is that some person "Pat" has been wiring lights up on the same set for 25 years and has been credited in 2500 movies, I do not think that too many people like this could potentially ruin the inherent fun the game and turn it into three degrees of separation. The first successful pass through the first degree took about 1.5 hours. This yielded a list of 4723 people that are in Kevin Bacon movies. The number 4723 caused much confusion as this is the ID number given to Kevin Bacon in TMdb's database, originally it was assumed that a logical error had been made. This theory was tested by changing the start point of the script to the ID of another person, this did not give the matching number of database entries (ID332 gave about 1400 records). The time it took to write down all of the people who have co-starred with a person was concerning, an hour and a half for one. At this point I started optimizing to speed the process up. Optimization starting with cleaning up the logic and lead to use of concurrent processing, which lead to further cleaning of the logic and additional checks to skip over redundant processing. A major change in the data structure during this phase helped tremendously. Originally I had intended to have a table for each degree and the entire route of each person included, this amount of redundant data appeared to grow very fast as I moved forward. The solution found was simply to list the person, a movie, and an ID in the previous degree linked as a foreign key. Not only did these changes to the database structure stop horizontal growth of the tables, but it also stopped the growth of the data structures within the program. An example is this: a person in the fifth degree would have ten entries in the database and ten pieces of information in the script to build the SQL statement to enter a single route, after the changes no matter the degree every SQL statement only needs three pieces of information to correctly construct the data structure. After optimization I was able to get the run time of recording co-stars to near ten seconds. This was deemed an acceptable amount of time and a separate script was constructed for each successive degree. Running the same algorithm that was run on Kevin Bacon for each person in the previous degree, this took about two hours to process all 4723 people with a credit in a Kevin Bacon movie. At the end of processing the second degree, 2,671 people in the first degree linked 444,699 to Kevin Bacon in the second degree and brings the total number of routes to 449,422. It becomes very clear when processing the second degree how much time was saved by implementing the multiprocessing functionality, for even at ten seconds per person this process took four days. processing the third degree, 56,741 people in the second degree link 1,017,296 to Kevin Bacon in the third degree and brings the total number of discovered routes to 1,466,718. The proportion of people from the database that have a route at this point is 78%.
      On a side bar, while figuring this proportion up I found that I had been looking at the wrong parts of my database. All of my work to this point has used only the credits table, and I had been using numbers from a different table. Turns out the database I thought was complete is not, there are more people IDs in the credits table than there are people in the person table. No adjustments should be needed as all the ID numbers in the credit table are valid within TMdb. However, now I see that there was no need to fill the person and movie table in my local database.



----------------------------
Skills developed from this project:
expanded SQL experience
concurrent.futures for running multiple processes

----------------------------
This is neat stuff I found while working on the project.
The source of all data used for this project:
https://www.themoviedb.org

Finding the oracle of bacon made me a little sad as I started work on this in a vacuum.
https://oracleofbacon.org/
Articles:
https://www.cnn.com/2014/03/08/tech/web/kevin-bacon-six-degrees-sxsw/
http://www.randalolson.com/2015/03/04/revisiting-the-six-degrees-of-kevin-bacon/
https://en.wikipedia.org/wiki/Small-world_network
Videos:
https://www.youtube.com/watch?v=Rmn-amJ9UA4
https://www.youtube.com/watch?v=n9u-TITxwoM&t=3s
https://www.youtube.com/watch?v=TcxZSmzPw8k&t=310s
