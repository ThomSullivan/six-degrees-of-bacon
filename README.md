# **Small World Network Mapping**
While I found this after conception of the idea, [The Oracle of Bacon](https://oracleofbacon.org/), has something very similar to what is available here. The biggest difference that exsists is this project moved more toward finding a connection for everyone to Kevin Bacon, where as [The Oracle of Bacon](https://oracleofbacon.org/) seems to find the route and then store it for later use. From a logical standpoint this mapping tool will move the opposite direction and record all routes starting with people in a Kevin Bacon movie.

The source of all data used for this project:
[The Movie Database](https://www.themoviedb.org)

Check out the notes file for thoughts and notes take while building this project

1. API key from [TMDb](https://www.themoviedb.org) is needed and can be added to the scraper and interface scripts to make them work.
2. Run the scraper and it will make a local database to use for tracing Bacon routes.
3. Run the degree scripts in order and one at a time to build the routes database for use with the interface.
4. The interface can be used as soon as the first degree finishes, you must make sure the list tables, inside of interface.py, matches the available tables in your routes database
