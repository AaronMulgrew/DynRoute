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
        if type(edges) != dict:
            raise TypeError("edges variable is not a dictionary.")
        else:
            self.edges = edges
            return True

    def reprocess_data(self, data):
        print data
        for key, value in data['junctions_edge'].iteritems():
            print value
        for element in data['junctions'].keys():
            print element

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