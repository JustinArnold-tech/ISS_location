import os
import re
import requests
from flask import Flask, render_template

server = Flask(__name__)
LOCATION_API_TOKEN = os.getenv('PRIVATE_TOKEN')
url = "http://api.open-notify.org/iss-now.json"
url2 = "http://api.open-notify.org/astros.json"

@server.route("/", methods=['GET'])
def iss_local():

    #Gets the latitude and longitude of the ISS
    req = requests.get(url)

    obj = req.json()
    lat = obj['iss_position']['latitude']
    lon = obj['iss_position']['longitude']
    
    #Takes the latitude and longitude and puts it into location api to find which country the ISS is over
    try:
        iss_local = requests.get(f'https://us1.locationiq.com/v1/reverse.php?key={PRIVATE_TOKEN}&lat={lat}&lon={lon}&format=json')
    except Exception as e:
        raise e
    
    iss_curr = iss_local.json()
    print(iss_curr)
    if 'address' in iss_curr:
        country = iss_curr['address']['country']
    else:
        country = "Over Water"

    #Gets the number of people currently in space
    req2 = requests.get(url2)
    
    obj2 = req2.json()
    cnt = obj2['number']

    #Renders to info to html
    return render_template("iss.html",country=country, lat=lat, lon=lon, cnt=cnt)
    

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)