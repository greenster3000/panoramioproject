#!/usr/bin/python
#coding: utf-8

# A simple program which asks for two 6-dp latitude and longitude co-ordinates
# and calucaltes the co-oridinates of 1 km square around this point
# It then does a wget from the Panoramio.com API, and returns the number
# of photos in this square km

# Author - j.alexander.green@googlemail.com

import wget, json, math
from pprint import pprint

earth_circ = 40030.0
km_in_lat = 360.0/earth_circ

print "\nFor latitudes and longitudes, input them to 6 decimal places"
print "The program will caluclate 1km square with this as the midpoint\n"
lat_start = float(raw_input("What is the starting latitude?  "))
long_start = float(raw_input("What is the starting longitude?  "))

lat_max = str(round(lat_start + km_in_lat/2.0, 6))
lat_min	= str(round(lat_start - km_in_lat/2.0, 6))

angle = math.cos(lat_start)
long_max = str(round(long_start + 180/(angle * earth_circ), 6))
long_min = str(round(long_start - 180/(angle * earth_circ), 6))

print "\nFinding photos between " + long_min + " and " + long_max + " degrees longitude"
print "...and between " + lat_min + " and " + lat_max + " degrees latitude\n"


url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=0&to=100&minx=" + long_min + "&miny=" + lat_min + "&maxx=" + long_max +"&maxy=" + lat_max+"&size=original&mapfilter=true"

result = wget.download(url)
json_data = open("get_panoramas.php")
data = json.load(json_data)
count = data["count"]
print "\n\nthe number of photos in this square km is: " + str(count) + "\n"
json_data.close()