import math
earth_circ = 40075.0 # circumference of the earth in km
km_in_lat = round(360.0/earth_circ, 6) # 1km in degrees latitude
print km_in_lat
print "\nFor latitudes and longitudes, input them to 6 decimal places"
print "The program will caluclate 1km square with this as the midpoint\n"
lat_end = 50.576631
long_start = -2.970453
lat_start = 50.928307
long_end = -1.923294

middle_lat = (lat_end+lat_start)/2.0
print "middle lat is " + str(middle_lat)
angle = math.cos(middle_lat*math.pi/180.0)
km_in_long = round(360.0/earth_circ/angle, 6) #1km in deg long
print "km in long is" + str(km_in_long)

lat_length = lat_start - lat_end
number_of_lat_squares = int(math.ceil(lat_length/km_in_lat))
print "number_of_lat_squares" + str(number_of_lat_squares)

long_length = (long_end - long_start)
number_of_long_squares = int(math.ceil(long_length/km_in_long))

print "number_of_long_squares" + str(number_of_long_squares)
lat_max = lat_start # lat_min and lat_max will be used to generate the url
lat_min = lat_start - km_in_lat # from the starting latitude and difference