from math import radians, sin, cos, atan2, sqrt


def get_distance_haversine(distance1, distance2):
    ### implementation of the haversine formula in python
    # get the radius in metres
    radius = 6371 * 1000 

    lat1 = distance1[0]
    lon1 = distance1[1]
    lat2 = distance2[0]
    lon2 = distance2[1]

    '''lat1 = 52.632930
    lon1 = -1.161572
    lat2 = 52.632912
    lon2 = -1.157873'''

    try:
        ## calculate the distance in latitude and longtiude in radians
        distanceLat = radians(lat2 - lat1)
        distanceLon = radians(lon2 - lon1)
    except TypeError:
        # this is incase unicode params are provided
        raise TypeError("Could not convert as variables are not floats")

    # cosine and sine transforms
    a = sin(distanceLat/2) * sin(distanceLat/2) \
        + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(distanceLon/2) * sin(distanceLon/2)
    
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # get the distance from the radius times by 
    # great circle distance in radians
    distanceMeters = radius * c
    return distanceMeters

