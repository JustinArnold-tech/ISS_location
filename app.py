import os
import requests
from pprint import pprint
from flask import Flask, render_template, request


server = Flask(__name__)
apiKey = os.getenv('apiKey')
POSTER_KEY = os.getenv("POSTER_KEY")

@server.route("/", methods=['Get', 'Post'])
def api_weather():
    
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
        pprint(poster_info)
        poster = poster_info['posters'][0]['link']
        return render_template('movie.html', poster=poster, **info)

    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)