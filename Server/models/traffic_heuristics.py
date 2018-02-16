def handle_time(route, time, traffic_load):
    if route[u'road_type'] == 3:
        time = time * 2

    if traffic_load >= 50:
        time = time * 3

    return time