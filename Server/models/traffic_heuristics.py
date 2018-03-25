## this is the component for the handling of the time aggregate 
# within the current state
def handle_time(route, time, traffic_load):

    if traffic_load < 5:
        time = time * 1.4

    # this will nearly double the time for realism
    time = time + (traffic_load * 2)

    # this is a top level cap to make sure that the numbers don't go crazy.
    if time > 150:
        time = 150
    return time