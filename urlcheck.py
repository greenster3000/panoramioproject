import requests

def add_photo(data, urls):
	for photo in data:
		if photo["photo_url"] not in urls:
			urls.append(photo["photo_url"])

url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=0&to=100&minx=-2.970453&miny=50.576631&maxx=-1.923294&maxy=50.928307&size=small&mapfilter=false" 

data = requests.get(url).json()
iterations = data["count"]/100
print "accoriding to the count variable there should be " + str(data["count"]) + " photos"

list_of_photo_urls = []
lower = 0
upper = 100

for i in range(iterations):
	url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=" + str(lower) + "&to=" + str(upper) + "&minx=-2.970453&miny=50.576631&maxx=-1.923294&maxy=50.928307&size=small&mapfilter=false" 
	print "finding photos numbered " + str(lower) + " to " + str(upper)
	data = requests.get(url).json()	
	add_photo(data["photos"], list_of_photo_urls)
	lower, upper = upper, upper + 100

print "but I can only find " + str(len(list_of_photo_urls))