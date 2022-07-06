from dis import dis
import re
from turtle import heading, width
from django.shortcuts import render, get_object_or_404
from .models import Measurements
from .forms import MeasurementsForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_centre_coordinates, get_proper_zoom
import folium
# Create your views here.

def calculateDistanceView(request):
    # obj = Measurements.objects.all()
    distance = None
    destination = None
    form = MeasurementsForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')
    
    ip = '45.123.218.33'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)
    
    # initial coordinates
    l_lat = lat
    l_lon = lon

    pointA = (l_lat, l_lon)

    # initial map
    m = folium.Map(width=600, height=350, location=get_centre_coordinates(l_lat, l_lon), zoom_start = 8)
    #location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'], icon
                    =folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data['destination']
        destination = geolocator.geocode(destination_)

        #destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat, d_lon)
        distance = round(geodesic(pointA, pointB).km, 2)

        #folium map modifaction
        m = folium.Map(width=600, height=350, location=get_centre_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_proper_zoom(distance))

        #location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'], icon
                    =folium.Icon(color='purple')).add_to(m)
        
        #destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination, icon
                    =folium.Icon(color='red', icon='cloud')).add_to(m)

        #draw the line between location and destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)

        # instance.location = location
        # instance.distance = distance
        # instance.save()
    
    m = m._repr_html_() #map as html representation

    context = {
        'distance': distance,
        'form' : form,
        'map': m,
        'location': location,
        'destination': destination
    }

    return render(request, 'measurements/main.html', context=context)