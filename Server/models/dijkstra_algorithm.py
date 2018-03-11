from collections import defaultdict
from scripts import haversine
from models import global_route
global_route = global_route.GlobalRouteHandler()
import Queue
import heapq

class Dijkstra():
    def __init__(self):
        self.edges = dict()
        self.start_node = False

    def set_edges(self, edges):
        self.edges = edges

    def reprocess_data(self, data):
        #print data
        time_dict = {}
        for key, value in data['junctions_edge'].iteritems():
            routes = value['routes'][0]
            source_lat, source_lon = key.split('//')
            time = global_route.calculate_junction_distance_time(source_lat, source_lon, value['speed'], routes, routes['traffic_load'])
            self.start_node = key
            time_dict[key] = [{'source':key, 'dest':routes['lat']+'//'+routes['lon'],'time':time}]
            #print value
            #self.edges[key] = time_dict
        for key in data['junctions'].keys():
            #print key
            one_junction = data['junctions'][key]
            #print one_junction
            source_lat, source_lon = key.split('//')
            for route in one_junction['routes']:
                if route:
                    #print one_junction
                    time = global_route.calculate_junction_distance_time(source_lat, source_lon, value['speed'], route, route['traffic_load'])
                    #time = route['time']
                    #make lat and lon one element
                    lat_lon = route['lat'] + '//' + route['lon']
                    #print route['time']
                    onetime = route['time']
                    if key in time_dict:
                        route = time_dict[key]
                        route.append({'source': key, 'dest': lat_lon, 'time': onetime})
                        time_dict[key] = route
                    else:
                        time_dict[key] = [{'source': key, 'dest': lat_lon, 'time': onetime}]
                #time_dict.append((key, lat_lon, time))
            #print time_dict
            #self.edges[key]= time_dict
        self.edges = time_dict
        #print self.edges[key]

    def compute_shortest_route(self, source, dest):
        edges = self.edges
        #print edges
        q = Queue.Queue()
        heap = []
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
            #heapq.heappush(heap, onejunc)

        #print q.queue
        #print time

        if self.start_node:
            source_node = self.edges[self.start_node]
            onedict = {'dest': source_node[0]['dest'], 'source': source_node[0]['source'], 'time': float("inf")}
            time[self.start_node] = onedict
            heapq.heappush(heap, self.edges[self.start_node])

        #qt = q.get()
        #print qt
        #qt = heapq.heappop(heap)
        #print qt
        while heap:
            # this is our vertex
            v = heapq.heappop(heap)
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
                    timenext = time[next]['time']
                    if vtime < timenext:
                        time[next] = {'source': previous, 'dest': next, 'time':vtime}
                        try:
                            heapq.heappush(heap, self.edges[next])
                        except KeyError:
                            break
                    #else:
                        #pass
                        #print "not needed" + str(vtime) + ' ' + str(timenext)
                #else:
                    #print 'not in key'

        route = list()
        nextitem = dest
        while time.get(nextitem) is not None:
            onenode = time[nextitem]
            if 'dest' in onenode:
                route.append(nextitem)
                nextitem = time[nextitem]['source']
                if nextitem == route[-1]:
                    nextitem = None
            else:
                break
            #print nextitem
        route.reverse()
        return {"route": route}