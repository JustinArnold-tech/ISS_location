import os
import requests
import logging as logg
from pprint import pprint
from flask import Flask, render_template, request

#you could also move these into constants.py
DEBUG = True
server = Flask(__name__)
apiKey = os.getenv('apiKey')
POSTER_KEY = os.getenv("POSTER_KEY")
LOG_FILE = 'events.log'

# good!
logg.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logg.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

@server.route("/", methods=['Get', 'Post'])
def api_movie():
    
    if request.method == 'POST':
        
        data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
        year = ''
        movie = request.form['movie'] 
        params = {
            't':movie,
            'type':'movie',
            'y':year,
            'plot':'full'
        }
        response = requests.get(data_URL,params=params).json()

        if DEBUG:
            logg.debug(movie)

        if movie == response["Title"]:
            logg.error(f"Unable to find movie")

        Title = response['Title']
        released = response['Released']
        Rating = response['Rated']
        Runtime = response['Runtime']
        Genre = response['Genre']
        Director = response['Director']
        Writer = response['Writer']
        Actors = response['Actors']
        Plot = response['Plot']
        Id = response['imdbID']
        
        info = { 
            'Title' : Title,
            'released' : released,
            'Rating' : Rating,
            'Runtime' : Runtime, 
            'Genre' : Genre,
            'Director' : Director,
            'Writer' : Writer,
            'Actors' : Actors,
            'Plot' : Plot,
        }
        try:
            poster_info = requests.get(f'https://imdb-api.com/en/API/Posters/{POSTER_KEY}/{Id}').json()
        except Exception as e:
            raise e

        if DEBUG:
            pprint(poster_info)
        poster = poster_info['posters'][0]['link']
        return render_template('movie.html', poster=poster, **info)

    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)