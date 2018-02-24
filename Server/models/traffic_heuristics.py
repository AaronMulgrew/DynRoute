## this is the component for the handling of the time aggregate 
# within the current state
def handle_time(route, time, traffic_load):

    # this will nearly double the time if the traffic is bad
    time = time + (traffic_load * 2)

    # this is a top level cap to make sure that the numbers don't go crazy.
    if time > 150:
        time = 150
    return time