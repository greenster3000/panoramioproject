#!/usr/bin/python
#coding: utf-8

# Integration of three previous programmes.
# Given a rectangular area, information from panoramio.com API
# is returned in a 1km by 1km grid.

# Author - j.alexander.green@googlemail.com

import math, requests, csv

def add_photos(data, photos, urls, co_ords):
	for photo in data:
		if photo["photo_url"] not in urls:
			photos.append(photo)
			urls.append(photo["photo_url"])
			to_append = str(photo["latitude"]) + ", " + str(photo["longitude"])
			co_ords.append(to_append)

def check_photos(long_min, long_max, lat_min, lat_max, data, years_array):
	number = 0
	users = 0
	user_ids = []
	for photo in data:
		if (long_min <= photo["longitude"] <= long_max) & (lat_max <= float(photo["latitude"]) <= lat_min):
			number += 1
			if photo["owner_id"] not in user_ids:
				users += 1
				user_ids.append(photo["owner_id"])
			year = int(photo['upload_date'][-4:])
			years_array[year][-1][-1] += 1
	return number, users


earth_circ = 40075.0 
km_in_lat = round(360.0/earth_circ, 6) # 1 km in degrees latitude

print "\nEnter 2 latitude and 2 longitudes, one by one, to 6 dp."

lat_start = float(raw_input("What is the most northerly extent of the area?  "))
lat_end = float(raw_input("What is the most southernly extent?  "))
long_start = float(raw_input("What is the most westerly?  "))
long_end = float(raw_input("Easterly?  "))

name = raw_input("What is the name of the file where you want to store this data?  ")

middle_lat = (lat_end+lat_start)/2.0
angle = math.cos(middle_lat*math.pi/180.0)
km_in_long = round(360/earth_circ/angle, 6) #1km in degrees longitude

lat_length = abs(lat_start - lat_end)
number_of_lat_squares = int(math.ceil(lat_length/km_in_lat))

long_length = abs(long_end - long_start)
number_of_long_squares = int(math.ceil(long_length/km_in_long))

url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=100&minx=" + str(long_start) + "&miny=" + str(lat_end) + "&maxx=" + str(long_end) + "&maxy=" + str(lat_start) + "&size=original&mapfilter=false" 
data = requests.get(url).json()
count = data["count"] # maybe use this later
iterations = count/100

co_ords = []
list_of_photos = []
urls = []
lower = 0
upper = 100

for i in range(iterations):
	url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=" + str(lower) + "&to=" + str(upper) + "&minx=" + str(long_start) + "&miny=" + str(lat_end) + "&maxx=" + str(long_end) + "&maxy=" + str(lat_start) + "&size=original&mapfilter=false" 
	print "finding photos numbered " + str(lower) + " to " + str(upper)
	data = requests.get(url).json()
	add_photos(data["photos"],list_of_photos,urls,co_ords)
	lower, upper = upper, upper + 100

overall_array = []
user_array = []
years_array = {}
for i in range (2005,2016):
	years_array[i] = []

lat_min = lat_start
lat_max = lat_start - km_in_lat
row = ["blank"]
dummy = long_start
for n in range(number_of_long_squares):
	row.append(round(dummy,6))
	dummy += km_in_long
overall_array.append(row)
user_array.append(row)
for year in years_array:
	years_array[year].append(row)

for n in range(number_of_lat_squares):
	long_min = long_start
	long_max = long_start + km_in_long 
	overall_row = [lat_min]
	user_row = [lat_min]
	for i in range(2005,2016):
		years_array[i].append([lat_min])

	for m in range(number_of_long_squares):	
		for i in range(2005,2016):
			years_array[i][-1].append(0)
		number_of_photos, number_of_users = check_photos(long_min, long_max, lat_min, lat_max, list_of_photos, years_array)
		overall_row.append(number_of_photos)
		user_row.append(number_of_users)
		long_min, long_max = long_max, long_max + km_in_long

	overall_array.append(overall_row)
	user_array.append(user_row)
	lat_min, lat_max = lat_max, lat_max - km_in_lat

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

csv_writer(overall_array,name+".csv")
csv_writer(user_array,name+"_by_id.csv")
for year in years_array:
	csv_writer(years_array[year],name+str(year)+".csv")

f = open(name + "_co_ords.txt", "w")
for line in co_ords:
	f.write(line)
	f.write("\n")
f.close()

f = open(name+".csv", 'a')
f.write("\n Number of photos per sq km starting at " + str(lat_start) + \
	" degrees latitude and " + str(long_start) + " degrees longitude " + \
	"\nand finishing at " +str(lat_end) + " degrees latitude " + \
	str(long_end) + " degrees longtitude\nLatitude intervals of " + \
	str(km_in_lat) + " and longitude of " + str(km_in_long))
f.close()
f = open(name+"_by_id.csv", 'a')
f.write("\n Number of uniqe photo uploaders per sq km starting at " + str(lat_start) + \
	" degrees latitude and " + str(long_start) + " degrees longitude " + \
	"\nand finishing at " +str(lat_end) + " degrees latitude " + \
	str(long_end) + " degrees longtitude\nLatitude intervals of " + \
	str(km_in_lat) + " and longitude of " + str(km_in_long))
f.close()
for year in years_array:
	f = open(name+str(year)+".csv", 'a')
	f.write("\n Number of photos per sq km per year starting at " + str(lat_start) + \
	" degrees latitude and " + str(long_start) + " degrees longitude " + \
	"\nand finishing at " +str(lat_end) + " degrees latitude " + \
	str(long_end) + " degrees longtitude\nLatitude intervals of " + \
	str(km_in_lat) + " and longitude of " + str(km_in_long))
f.close()