from collections import defaultdict
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

    def process_path(self, cost, path, element=[]):
        if isinstance(path[1], tuple):
            element.append(path[0])
            self.process_path(cost, path[1], element)
        else:
            element.append(path[0])
            return element
        return element

    def compute_shortest(self, source, destination):
        nodelist = dict()
        edges = self.edges
        # create our own dict with each entry
        # named differently to parameters
        for each_source, each_destination, distance in edges:
            # create new instance of edgeitem class
            item = EdgeItem(each_destination, distance)
            # create a dictionary full of lists
            if nodelist.get(each_source) is not None:
                nodelist[each_source].append(item)
            else:
                itemlist = list()
                itemlist.append(item)
                nodelist[each_source] = itemlist

        # populate the heap with init values
        queue, seen = [(0,source,[])], set()
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
                path = (node, path)
                #path2 = path2.append(v1)
                if node == destination:
                    path = self.process_path(cost, path)
                    # we have to reverse the path as the algorithm
                    # discovers back to front.
                    return [cost, list(reversed(path))]
                for item in nodelist[node]:
                    if item.destination not in seen:
                        heapq.heappush(queue, (cost+item.distance, item.destination, path))

        return "no path found"

def compute_shortest2(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen = [(0,f,())], set()
    while q:
        (cost,v1,path) = heapq.heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: 
                return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                   heapq.heappush(q, (cost+c, v2, path))

    return float("inf")