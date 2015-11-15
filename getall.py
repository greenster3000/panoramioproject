import requests
sizes = [
    "original",
    "medium",
    "small",
    "thumbnail",
    "square",
    "mini_square"
]
lower = 1000
upper = 1005
url_true = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=" + str(lower) + "&to=" + str(upper) + "&minx=-2.970453&miny=50.576631&maxx=-1.923294&maxy=50.928307&size=original&mapfilter=true"
data = requests.get(url_true).json()
while data["has_more"]:
	lower, upper = upper, upper + 5
	print "getting photos " + str(lower) + " to " + str(upper)
	data = requests.get(url_true).json()
	print data["has_more"]
	print data["count"]
	print data["photos"]
