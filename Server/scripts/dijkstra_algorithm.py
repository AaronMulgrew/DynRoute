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

    def add_edges(self, edges):
        if type(edges) != list:
            raise TypeError("edges variable is not a list.")
        else:
            self.edges = edges
            return True

    def add_node(self, lat, lon):
        self.nodes.add(lat + "//" + lon)
        print self.nodes

    def compute_shortest(self, source, destination):
        nodelist = dict()
        edges = self.edges
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
            # pop the smallest item from the queue
            item = heapq.heappop(queue)
            # cost of retrieving the item
            cost = item[0]
            # this is the node of the value
            # if node is the same as the starting node
            # cost will be 0
            node = item[1]
            path = item[2]
            if node not in seen:
                seen.add(node)
                #path = [v1, path]
                path.add(node)
                #path2 = path2.append(v1)
                if node == destination:
                    return cost, path
                for item in nodelist[node]:
                    if item.destination not in seen:
                        heapq.heappush(queue, (cost+item.distance, item.destination, path))

                #for c, v2 in nodelist.get(v1, ()):
                #    if v2 not in seen:
                #        heapq.heappush(queue, (cost+c, v2, path))

        return "no path found"

