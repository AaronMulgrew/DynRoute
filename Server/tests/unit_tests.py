import unittest
import sys, os
from scripts import haversine
from scripts import dijkstra_algorithm
from scripts import API_auth
import server as server


class test_emergency_handler(unittest.TestCase):
    def test_emergency(self):
        emergency = server.EmergencyHandler()
        emergency.generate_emergency()

class test_haversine(unittest.TestCase):
    def test_haversine(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 249.6400152128023
        self.assertEqual(haversine.get_distance_haversine([52.632930, -1.161572], [52.632912, -1.157873]), distance)

    def test_haversine_min(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 1.1119492664455877
        lat1 = 0.00000
        lon1 = 0.00000
        lat2 = 0.00000
        lon2 = 0.00001
        self.assertEqual(haversine.get_distance_haversine([lat1, lon1], [lat2, lon2]), distance)

    def test_haversine_max(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 10007543.398010286
        lat1 = 0.00000
        lon1 = 0.00000
        lat2 = 90
        lon2 = -180
        x = haversine.get_distance_haversine([lat1, lon1], [lat2, lon2])
        self.assertEqual(haversine.get_distance_haversine([lat1, lon1], [lat2, lon2]), distance)

    def test_haversine_invalid(self):
        lat1 = "zzzzz"
        lon1 = "xxxxx"
        lat2 = 90
        lon2 = -180
        # this test checks that the Exception that is raised
        # also matches with the error message.
        self.assertRaisesRegexp(TypeError, "Could not convert as variables are not floats", haversine.get_distance_haversine, [lat1, lon1], [lat2, lon2])

class test_dijkstra(unittest.TestCase):

    def test_dijkstra_general(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = [
            ("A", "B", 7),
            ("A", "D", 5),
            ("B", "C", 8),
            ("B", "D", 9),
            ("B", "E", 7),
            ("C", "E", 5),
            ("D", "E", 15),
            ("D", "F", 6),
            ("E", "F", 8),
            ("E", "G", 9),
            ("F", "G", 11)
        ]
        dijkstra.add_edges(edges)

        route = dijkstra.compute_shortest("A", "E")
        print route

    def test_dijsktra_output_format(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = [
            ("A", "B", 7),
            ("A", "D", 5),
            ("B", "C", 8),
            ("B", "D", 9),
            ("B", "E", 7),
            ("C", "E", 5),
            ("D", "E", 15),
            ("D", "F", 6),
            ("E", "F", 8),
            ("E", "G", 9),
            ("F", "G", 11)
        ]
        dijkstra.add_edges(edges)

        route = dijkstra.compute_shortest("A", "E")
        self.assertEqual([14, ['A', 'B', 'E', 'A', 'B', 'E']], route)

    def test_dijkstra_add_edges_invalid(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = {}
        # this test checks that the Exception that is raised
        # also matches with the error message.
        self.assertRaisesRegexp(TypeError, "edges variable is not a list.", dijkstra.add_edges, edges)

    def test_dijkstra_add_edges_valid(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = [
            ("A", "B", 7),
            ("A", "D", 5),
            ("B", "C", 8),
            ("B", "D", 9),
            ("B", "E", 7),
            ("C", "E", 5),
            ("D", "E", 15),
            ("D", "F", 6),
            ("E", "F", 8),
            ("E", "G", 9),
            ("F", "G", 11)
        ]
        # this test checks that the add edges function is ok.
        self.assertTrue(dijkstra.add_edges(edges))

class test_server(unittest.TestCase):
    def test_server_junction_handler(self):
        newserver = server
        newserver.GetRoutes()
        junc = newserver.JunctionHandler()
        self.assertIsInstance(junc, newserver.JunctionHandler)

    def test_server_process_latlon(self):
        # check that the latlon function actually splits the latitude and longitude.
        newserver = server
        newserver.GetRoutes()
        junc = newserver.JunctionHandler()
        latlon = junc.process_lat_lon('120//-1')
        self.assertEqual(latlon, ('120', '-1'))

    def test_weighted_choice(self):
        newserver = server
        newserver.GetRoutes()
        junc = server.JunctionHandler()
        choice = junc.weighted_choice([[0, 50], [1, 15]])
        self.assertTrue(0 <= choice <= 1)

    def test_server_route_handler(self):
        newserver = server
        newserver.GetRoutes()
        junc = newserver.GlobalRouteHandler()
        self.assertIsInstance(junc, newserver.GlobalRouteHandler)

    def test_server_calc_distance_time(self):
        object = {u'lat': u'52.632912', u'lon': u'-1.157873', u'road_type': 1}
        estimatedTime = 4.160666920213371
        newserver = server
        newserver.GetRoutes()
        junc = server.JunctionHandler()
        choice = junc.calculate_junction_distance_time(object, traffic_load=40)
        print choice
        self.assertTrue(choice, 5.2008336502667145)

    def test_pick_random_edge_route(self):
        newserver = server
        newserver.GetRoutes()
        junc = server.JunctionHandler()
        choice = junc.pick_random_edge_route()
        # make sure we are producing something which is a valid python list.
        self.assertIsInstance(choice, list)

class test_API_auth(unittest.TestCase):
    def test_encode(self):
        # this test tests the encode method for the JWT token
        username = "Aaron"
        password = 123456
        encoded = API_auth.encode(username, password)
        self.assertIsInstance(encoded, str)

if __name__ == '__main__':
    unittest.main()
