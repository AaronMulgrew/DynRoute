import unittest
import sys, os
from scripts import haversine
import server as server

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


if __name__ == '__main__':
    unittest.main()
