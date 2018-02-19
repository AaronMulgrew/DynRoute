def handle_time(route, time, traffic_load):
    if route[u'road_type'] == 3 and traffic_load >= 10:
        time = time * 2.5

    elif route[u'road_type'] == 1 and traffic_load >= 10:
        time = time * 1.5

    if traffic_load >= 40:
        time = time * 2.5

    return time