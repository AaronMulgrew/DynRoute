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
        timeList = {}
        for key, value in data['junctions_edge'].iteritems():
            routes = value['routes']
            for one_route in routes:
                time = one_route['time']
                #make lat and lon one element
                lat_lon = one_route['lat'] + '//' + one_route['lon']
                if key in timeList:
                    route = timeList[key]
                    newtimeList = timeList[key].append({'source': key, 'dest': lat_lon, 'time': time})
                    timeList[key] = newtimeList
                else:
                    timeList[key] = [{'source': key, 'dest': lat_lon, 'time': time}]
            print value
            #self.edges[key] = timeList
        for key in data['junctions'].keys():
            print key
            one_junction = data['junctions'][key]
            print one_junction
            for route in one_junction['routes']:
                if route:
                    time = route['time']
                    #make lat and lon one element
                    lat_lon = route['lat'] + '//' + route['lon']
                    if key in timeList:
                        route = timeList[key]
                        route.append({'source': key, 'dest': lat_lon, 'time': time})
                        timeList[key] = route
                    else:
                        timeList[key] = [{'source': key, 'dest': lat_lon, 'time': time}]
                #timeList.append((key, lat_lon, time))
            print timeList
            #self.edges[key]= timeList
        self.edges = timeList
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
        for edge in edges:
            oneedge = edges[edge]
            print oneedge
            q.put(oneedge)
        # this is our source time dictionary
        # will be used to fill times to get to dest
        time = dict()
        for elem in list(q.queue):
            # this is our vertex
            v = q.get()
            for node in v:
                # cannot call it source and dest as only
                # iterating over one node
                previous = node['source']
                next = node['dest']
                junc_time = node['time']
                # here we check to see that there is a previous node
                if next in time.keys() and previous in time.keys():
                    element = time[previous]
                    vtime = time[previous]['time'] + junc_time
                    if vtime < time[next]:
                        time[next] = {'source': previous, 'dest': next, 'time':vtime}
                else:
                    # this means that it is a edge node, hence no time penalty
                    if previous not in time.keys():
                        time[previous] = {'source': previous, 'time': 0}
                    # otherwise treat it as normal (No cost as no previous)
                    time[next] = {'source': previous, 'dest': next, 'time': junc_time}
                print node
            print oneedge
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
        print route
        return route