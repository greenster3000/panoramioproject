#!/usr/bin/python
#coding: utf-8

# A simple program which asks for two 6-dp latitude and longitude co-ordinates
# and calucaltes the co-oridinates of 1 km square around this point
# It then does a wget from the Panoramio.com API, and returns the number
# of photos in this square km

# Author - j.alexander.green@googlemail.com

import requests, math, csv # libraries that the code will use

earth_circ = 40075.0 # circumference of the earth in km
km_in_lat = round(360.0/earth_circ, 6) # 1km in degrees latitude

print "\nInput four individual 6 decimal place points (i.e. 1 per prompt)"
print "The program will caluclate the number of photos taken per year per sq km.\n"
lat_end = float(raw_input("What is the most southernly extent of the area?  "))
long_start = float(raw_input("What is the most westerly extent?  "))
lat_start = float(raw_input("Most northerly?  "))
long_end = float(raw_input("Easterly?  "))

name = raw_input("What is the name of the file where you want to store this data?  ")

middle_lat = (lat_end+lat_start)/2.0
angle = math.cos(middle_lat*math.pi/180.0)
km_in_long = round(360.0/earth_circ/angle, 6) #1km in deg long

lat_length = lat_start - lat_end
number_of_lat_squares = int(math.ceil(lat_length/km_in_lat))

long_length = (long_end - long_start)
number_of_long_squares = int(math.ceil(long_length/km_in_long))

lat_max = lat_start # lat_min and lat_max will be used to generate the url
lat_min = lat_start - km_in_lat # from the starting latitude and difference

# using two loops to go cycle through each square longitude in the inside loop
# and latitude in the outside loop
years = {}
for i in range (2005,2016):
	years[i] = []

naughty_photos = 0
for n in range(number_of_lat_squares):
	long_min = long_start 
	long_max = long_start + km_in_long
	for i in range(2005,2016):
		years[i].append([])
	for m in range(number_of_long_squares):
		for i in range(2005,2016):
			years[i][-1].append(0)
		print "\nFinding photos between " + str(long_min) + " and " + str(long_max) + " degrees longitude"
		print "...and between " + str(lat_max) + " and " + str(lat_min) + " degrees latitude\n"
		url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=0&to=100&minx=" + str(long_min) + "&miny=" + str(lat_min) + "&maxx=" + str(long_max) +"&maxy=" + str(lat_max) +"&size=original&mapfilter=false"
		data = requests.get(url).json()	
		if data["photos"]:
			print "there are photos!"
			print str(len(data["photos"])) + " of them!"
			for photo in data["photos"]:
				year = int(photo['upload_date'][-4:])
				print "the year is: " + str(year)
				latitude = photo['latitude']
				longitude = photo['longitude']
				if ((lat_min < latitude) & (latitude < lat_max) & (long_min < longitude) & (longitude < long_max)):
					years[year][-1][-1] += 1
				else:
					print "naughty photo!"
					naughty_photos += 1
		long_min, long_max = long_max, long_max + km_in_long
	lat_max, lat_min = lat_min, lat_min - km_in_lat
print "there were " + str(naughty_photos) + " naughty photos"
def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

for year in years:
	csv_writer(years[year],name+str(year)+".csv")

	f = open(name+str(year)+".csv", 'a')
	f.write("\n Photos per 1km square starting at " + str(lat_start) + \
		" degrees latitude and " + str(long_start) + " degrees longitude " + \
		"\nand finishing at " +str(lat_end) + " degrees latitude " + \
		str(long_end) + " degrees longtitude\nLatitude intervals of " + \
		str(km_in_lat) + " and longitude of " + str(km_in_long))
	f.close()