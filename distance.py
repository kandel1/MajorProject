from geopy.distance import vincenty
	
def calculatedistance(long1, lat1, long2, lat2):
	costumer = (lat1,long1 )
	taxi = (lat2, long2 )
	distance = vincenty(costumer, taxi).km
	return distance
