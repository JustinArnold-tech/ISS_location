import os
import re
import requests
from flask import Flask, render_template

server = Flask(__name__)
PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')
url = "http://api.open-notify.org/iss-now.json"
url2 = "http://api.open-notify.org/astros.json"

@server.route("/", methods=['GET'])
def iss_local():

    req = requests.get(url)

    obj = req.json()
    lat = obj['iss_position']['latitude']
    lon = obj['iss_position']['longitude']
    # print(lat, lon)
    try:
        iss_local = requests.get(f'https://us1.locationiq.com/v1/reverse.php?key={PRIVATE_TOKEN}&lat={lat}&lon={lon}&format=json')
    except Exception as e:
        raise e
    
    iss_curr = iss_local.json()
    # print(iss_curr)
    if 'address' in iss_curr:
        state = iss_curr['address']['state']
        country = iss_curr['address']['country']
    else:
        state = "Over"
        country = "Water"

    req2 = requests.get(url2)
    
    obj2 = req2.json()
    cnt = obj2['number']

    return render_template("iss.html",country=country, state=state, lat=lat, lon=lon, cnt=cnt)
    
        

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)