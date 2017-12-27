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

    def compute_shortest(self):
        route = set()
        route.add(0)
        return route

c = Dijkstra()
c.add_node("1212.121", "1212.11")
x = c.compute_shortest()
print x