from skyfield.api import load, N, S, E, W, wgs84
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['POST'])
def moon_distance():
    content = request.json

    latitude = content['latitude']
    longitude = content['longitude']

    return calculate_moon_distance(latitude, longitude)


def calculate_moon_distance(latitude, longitude):
    ts = load.timescale()
    t = ts.now()

    if latitude > 0:
        latitude_direction = N
    else:
        latitude_direction = S

    if longitude > 0:
        longitude_direction = E
    else:
        longitude_direction = W

    planets = load('de421.bsp')
    earth, moon = planets['earth'], planets['moon']

    location = earth + wgs84.latlon(latitude * latitude_direction, longitude * longitude_direction, elevation_m=43)
    astro = location.at(t).observe(moon)

    ra, dec, distance = astro.radec()

    return "{:.2f}".format(distance.km)
