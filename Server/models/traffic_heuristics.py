def handle_time(route, time, traffic_load):
    #time = time * traffic_load
    #if route[u'road_type'] == 3:
    #    time = time * traffic_load

    #elif route[u'road_type'] == 1 and traffic_load >= 10:
    #    time = time * 1.5

    time = time + traffic_load

    #if traffic_load >= 60:
    #    time = time + 808080

    return time