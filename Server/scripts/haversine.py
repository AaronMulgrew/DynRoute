from math import radians, sin, cos, atan2, sqrt


def get_distance_haversine(lat_lon_list):
    ### implementation of the haversine formula in python
    # get the radius of the earth in metres
    radius = 6371 * 1000 

    source_lat = lat_lon_list[0]
    source_lon = lat_lon_list[1]
    dest_lat = lat_lon_list[2]
    dest_lon = lat_lon_list[3]

    # checks to see if all items in the list are unicode
    if all(isinstance(item, unicode) for item in lat_lon_list):
        source_lat = float(source_lat)
        source_lon = float(source_lon)
        dest_lat = float(dest_lat)
        dest_lon = float(dest_lon)

    try:
        ## calculate the distance in latitude and longtiude in radians
        distanceLat = radians(dest_lat - source_lat)
        distanceLon = radians(dest_lon - source_lon)
    except TypeError:
        # this is incase unicode params are provided
        raise TypeError("Could not convert as variables are not floats")

    # cosine and sine transforms
    a = sin(distanceLat/2) * sin(distanceLat/2) \
        + cos(radians(source_lat)) \
        * cos(radians(dest_lat)) * sin(distanceLon/2) * sin(distanceLon/2)
    
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # get the distance from the radius times by 
    # great circle distance in radians
    distanceMeters = radius * c
    return distanceMeters

