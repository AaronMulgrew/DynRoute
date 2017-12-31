import heapq

class EdgeItem:
    def __init__(self, destination, distance):
        self.destination = destination
        self.distance = distance


class Dijkstra():
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.weighting = dict()
        print "not Implemented yet"

    def add_edge(self):
        print "#####"

    def add_node(self, lat, lon):
        self.nodes.add(lat + "//" + lon)
        print self.nodes

    def compute_shortest(self, edges, source, destination):
        nodelist = dict()
        # create our own dict with each entry
        for source, destination, distance in edges:
            # create new instance of edgeitem class
            item = EdgeItem(destination, distance)
            # create a dictionary full of lists
            if nodelist.get(source) is not None:
                nodelist[source].append(item)
            else:
                itemlist = list()
                itemlist.append(item)
                nodelist[source] = itemlist

        # populate the heap with init values
        queue, seen = [(0,source,set())], set()
        while queue:
            #(cost,v1, path) = heapq.heappop(queue)
            item = heapq.heappop(queue)
            cost = item[0]
            v1 = item[1]
            path = item[2]
            if v1 not in seen:
                seen.add(v1)
                #path = [v1, path]
                path.add(v1)
                #path2 = path2.append(v1)
                if v1 == destination:
                    return cost, path
                for item in nodelist[v1]:
                    if item.destination not in seen:
                        heapq.heappush(queue, (cost+item.distance, item.destination, path))

                #for c, v2 in nodelist.get(v1, ()):
                #    if v2 not in seen:
                #        heapq.heappush(queue, (cost+c, v2, path))

        return float("inf")

