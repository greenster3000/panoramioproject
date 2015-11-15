#!/usr/bin/python
#coding: utf-8

# A simple program which asks for two 6-dp latitude and longitude co-ordinates
# and calucaltes the co-oridinates of 1 km square around this point
# It then does a wget from the Panoramio.com API, and returns the number
# of photos in this square km

# Author - j.alexander.green@googlemail.com

import math, requests, csv # libraries that the code will use

earth_circ = 40075.0 # circumference of the earth in km
km_in_lat = round(360.0/earth_circ, 6) # 1km in degrees latitude

print "\nFor latitudes and longitudes, input them to 6 decimal places"
print "The program will caluclate 1km square with this as the midpoint\n"
lat_end = float(raw_input("What is the most southernly extent of the area?  "))
long_start = float(raw_input("What is the most westerly extent?  "))
lat_start = float(raw_input("Most northerly?  "))
long_end = float(raw_input("Easterly?  "))

name = raw_input("What is the name of the file where you want to store this data?  ")

middle_lat = (lat_end+lat_start)/2.0
angle = math.cos(middle_lat*math.pi/180.0)
km_in_long = round(360/earth_circ/angle, 6) #1km in deg long

lat_length = lat_start - lat_end
number_of_lat_squares = int(math.ceil(lat_length/km_in_lat))

long_length = long_end - long_start
number_of_long_squares = int(math.ceil(long_length/km_in_long))

lat_max = lat_start # lat_min and lat_max will be used to generate the url
lat_min = lat_start - km_in_lat # from the starting latitude and difference

# using two loops to go cycle through each square longitude in the inside loop
# and latitude in the outside loop

array = []
for n in range(number_of_lat_squares):
	long_min = long_start # re-setting the values for each loop
	long_max = long_start + km_in_long 
	row = []
	for m in range(number_of_long_squares):
		user_ids = []
		row.append(0)
		print "\nFinding unique photo uploaders between " + str(long_min) + " and " + str(long_max) + " degrees longitude"
		print "...and between " + str(lat_max) + " and " + str(lat_min) + " degrees latitude"
		url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=0&to=100&minx=" + str(long_min) + "&miny=" + str(lat_min) + "&maxx=" + str(long_max) +"&maxy=" + str(lat_max) +"&size=original&mapfilter=false"		
		data = requests.get(url)
		data = data.json()
		if data["photos"]:
			for photo in data["photos"]:
				if photo["owner_id"] not in user_ids:
					row[-1] += 1
					user_ids.append(photo["owner_id"])
					print "found a new user, adding their user id (=" + str(photo["owner_id"]) + ") to the list"
				elif photo["owner_id"] in user_ids:
					print "we've already counted user" + str(photo["owner_id"]) + "in this square"
				else:
					print "we shouldn't see this"
		long_min, long_max = long_max, long_max + km_in_long #increments the longitude parameters for the next cycle
	array.append(row)
	lat_max, lat_min = lat_min, lat_min	- km_in_lat # after one complete longitude cycle, increments the latitude

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

csv_writer(array,name+"by_id.csv")

f = open(name+".csv", 'a')
f.write("\n Number of unique photo uploaders per sq km starting at " + str(lat_start) + \
	" degrees latitude and " + str(long_start) + " degrees longitude " + \
	"\nand finishing at " +str(lat_end) + " degrees latitude " + \
	str(long_end) + " degrees longtitude\nLatitude intervals of " + \
	str(km_in_lat) + " and longitude of " + str(km_in_long))
f.close()