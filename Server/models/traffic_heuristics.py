def handle_time(route, time, traffic_load):
    #time = time + traffic_load

    time = time + (traffic_load * 2)

    return time