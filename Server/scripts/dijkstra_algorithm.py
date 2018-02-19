from collections import defaultdict
import haversine
import Queue

class EdgeItem:
    def __init__(self, destination, distance):
        self.destination = destination
        self.distance = distance


class Dijkstra():
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.weighting = dict()

    def add_edges(self, edges):
        if type(edges) != dict:
            raise TypeError("edges variable is not a dictionary.")
        else:
            self.edges = edges
            return True

    def reprocess_data(self, data):
        print data
        time_dict = {}
        for key, value in data['junctions_edge'].iteritems():
            routes = value['routes']
            for one_route in routes:
                time = one_route['time']
                #make lat and lon one element
                lat_lon = one_route['lat'] + '//' + one_route['lon']
                if key in time_dict:
                    route = time_dict[key]
                    newtimeList = time_dict[key].append({'source': key, 'dest': lat_lon, 'time': time})
                    time_dict[key] = newtimeList
                else:
                    time_dict[key] = [{'source': key, 'dest': lat_lon, 'time': time}]
            print value
            #self.edges[key] = time_dict
        for key in data['junctions'].keys():
            print key
            one_junction = data['junctions'][key]
            print one_junction
            for route in one_junction['routes']:
                if route:
                    time = route['time']
                    #make lat and lon one element
                    lat_lon = route['lat'] + '//' + route['lon']
                    if key in time_dict:
                        route = time_dict[key]
                        route.append({'source': key, 'dest': lat_lon, 'time': time})
                        time_dict[key] = route
                    else:
                        time_dict[key] = [{'source': key, 'dest': lat_lon, 'time': time}]
                #time_dict.append((key, lat_lon, time))
            print time_dict
            #self.edges[key]= time_dict
        self.edges = time_dict
        #print self.edges[key]

    # this flattens the tuple into a format more 
    # easily supportable (list)
    def process_path(self, cost, path, element=[]):
        if isinstance(path[1], tuple):
            element.append(path[0])
            self.process_path(cost, path[1], element)
        else:
            element.append(path[0])
            return element
        return element

    def compute_shortest_route(self, source, dest):
        edges = self.edges
        print edges
        q = Queue.Queue()
        # this is our source time dictionary
        # will be used to fill times to get to dest
        time = dict()
        for edge in edges:
            onejunc = edges[edge]
            for oneroute in onejunc:
                destination = oneroute['dest']
                onedict = {'dest': oneroute['dest'], 'source': oneroute['source'], 'time': float("inf")}
                #dest_source = oneroute['dest'] + '--' + oneroute['source']
                time[destination] = onedict
            q.put(onejunc)

        print q.queue
        print time

        for elem in list(q.queue):
            # this is our vertex
            v = q.get()
            for node in v:
                # cannot call it source and dest as only
                # iterating over one node
                previous = node['source']
                next = node['dest']
                junc_time = node['time']
                #match_next = filter(lambda time: time['dest'] == next, time)
                # here we check to see that the node is in the time dictionary
                if next in time.keys():
                    #match_previous = filter(lambda time: time['source'] == previous and time['dest'] == dest, time)
                    if previous in time.keys():
                        element = time[previous]
                        if element['time'] == float("inf"):
                            vtime = junc_time
                        else:
                            vtime = element['time'] + junc_time
                    else:
                        # no previous so cost is 0
                        time[previous] = {'source': previous, 'time': 0}
                        vtime = junc_time
                    timenext = time[dest]['time']
                    if vtime < timenext:
                        time[next] = {'source': previous, 'dest': next, 'time':vtime}
                    else:
                        print "not needed" + str(vtime) + ' ' + str(timenext)
                else:
                    print 'not in key'

                #else:
                #    # this means that it is a edge node, hence no time penalty
                #    if previous not in time.keys():
                #        time[previous] = {'source': previous, 'time': 0}
                #    # otherwise treat it as normal (No cost as no previous)
                #    time[next] = {'source': previous, 'dest': next, 'time': junc_time}
                print node
        print time

        route = list()
        nextitem = dest
        while time.get(nextitem) is not None:
            onenode = time[nextitem]
            if 'dest' in onenode:
                route.append(nextitem)
                nextitem = time[nextitem]['source']
            else:
                break
            print nextitem
        route.reverse()
        return route