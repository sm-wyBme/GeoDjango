#helper functions
from django.contrib.gis.geoip2 import GeoIP2

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

#to get the centre coordinates 
def get_centre_coordinates(latA, lonA, latB=None, lonB=None):
    cord = (latA, lonA)
    if latB:
        cord = [(latA+latB)/2, (lonA+lonB)/2]
    return cord

#proper zoom
def get_proper_zoom(distance):
    if distance <= 100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2