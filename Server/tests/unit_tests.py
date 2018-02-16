import unittest
import sys, os
import json
import datetime
import all_routes
from scripts import haversine
from models import junction_handler, emergency_route, global_route
from scripts import dijkstra_algorithm
from scripts import API_auth
try:
    import server as server
except ImportError:
    sys.path.insert(0, os.path.abspath(".."))
    from Server import server
#from server import app
#from app import app


class test_flask_endpoints(unittest.TestCase): 
    def setUp(self):
        # creates a test client
        self.app = server.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def test_gen_route(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')
        assert result.status_code == 200

    def test_gen_route_json(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')
        data = json.loads(result.data)
        # make sure that there is a latitude key in the dict
        assert 'lat' in data
        assert 'lon' in data


    def test_gen_next_route(self):
        result = self.app.get('coordinates/52.632912:-1.157873')
        assert result.status_code == 200

    def test_gen_next_route_json(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/52.632912:-1.157873')
        data = json.loads(result.data)
        # make sure that there is a latitude key in the dict
        assert 'lat' in data
        assert 'lon' in data


    def test_generate_emergency_no_auth_token_resp_message(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/generate_emergency')
        self.assertEqual(result.data, "No auth token")

    def test_generate_emergency_no_auth_token_resp_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/generate_emergency')
        self.assertEqual(result.status_code, 401)


    def test_generate_emergency_wrong_auth_token_resp_message(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/generate_emergency')
        self.assertEqual(result.data, "No auth token")

class test_all_routes(unittest.TestCase):
    def setUp(self):
        self.allroutes = all_routes.AllRoutes()
        self.junction_data = self.allroutes.grab_junction_data()

    def test_valid_add_junction(self):
        time = datetime.datetime.now()
        coords = ["1111","2222"]
        result = self.allroutes.add_junction_data(time, coords)
        self.assertTrue(result)

    def test_invalid_pop_route(self):
        time = datetime.datetime.now()
        returnvar = self.allroutes.pop_route(time)
        self.assertFalse(returnvar)

    def test_valid_pop_route(self):
        time = datetime.datetime.now()
        coords = ["1111","2222"]
        self.allroutes.add_junction_data(time, coords)
        #self.allroutes.junction_data[current_datetime] = coords
        returnvar = self.allroutes.pop_route(time)
        self.assertTrue(returnvar)

    def test_update_traffic_load_invalid(self):
        coords = ["1111", "2222"]
        traffic_load = 24
        returnvar = self.allroutes.update_traffic_load(coords, traffic_load)
        self.assertFalse(returnvar)

class test_emergency_handler(unittest.TestCase):
    def test_emergency(self):
        emergency = emergency_route.EmergencyHandler()
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
        edges = {
            "1":("A", "B", 7),
            "2":("A", "D", 5),
            "3":("B", "C", 8),
            "4":("B", "D", 9),
            "5":("B", "E", 7),
            "6":("C", "E", 5),
            "7":("D", "E", 15),
            "8":("D", "F", 6),
            "9":("E", "F", 8),
            "10":("E", "G", 9),
            "11":("F", "G", 11)
        }
        dijkstra.add_edges(edges)

        #route = dijkstra.compute_shortest("A", "E")
        #print route

    def test_dijsktra_output_format(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = {
            "1":("A", "B", 7),
            "2":("A", "D", 5),
            "3":("B", "C", 8),
            "4":("B", "D", 9),
            "5":("B", "E", 7),
            "6":("C", "E", 5),
            "7":("D", "E", 15),
            "8":("D", "F", 6),
            "9":("E", "F", 8),
            "10":("E", "G", 9),
            "11":("F", "G", 11)
        }
        dijkstra.add_edges(edges)

        #route = dijkstra.compute_shortest("A", "E")
        #self.assertEqual([14, ['A', 'B', 'E', 'A', 'B', 'E']], route)

    def test_dijkstra_add_edges_invalid(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = []
        # this test checks that the Exception that is raised
        # also matches with the error message.
        self.assertRaisesRegexp(TypeError, "edges variable is not a dictionary.", dijkstra.add_edges, edges)

    def test_dijkstra_add_edges_valid(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = {
            "1":("A", "B", 7),
            "2":("A", "D", 5),
            "3":("B", "C", 8),
            "4":("B", "D", 9),
            "5":("B", "E", 7),
            "6":("C", "E", 5),
            "7":("D", "E", 15),
            "8":("D", "F", 6),
            "9":("E", "F", 8),
            "10":("E", "G", 9),
            "11":("F", "G", 11)
        }
        # this test checks that the add edges function is ok.
        self.assertTrue(dijkstra.add_edges(edges))

class test_server(unittest.TestCase):

    def setUp(self):
        self.JunctionHandler = junction_handler.JunctionHandler()
        self.GlobalRoute = global_route.GlobalRouteHandler()
        return super(test_server, self).setUp()

    def test_server_junction_handler(self):
        junc = self.JunctionHandler
        class_file = junction_handler
        self.assertIsInstance(junc, class_file.JunctionHandler)

    def test_server_process_latlon(self):
        # check that the latlon function actually splits the latitude and longitude.
        junc = self.JunctionHandler
        latlon = junc.process_lat_lon('120//-1')
        self.assertEqual(latlon, ('120', '-1'))

    def test_weighted_choice(self):
        junc = self.JunctionHandler
        choice = junc.weighted_choice([[0, 50], [1, 15]])
        self.assertTrue(0 <= choice <= 1)

    def test_server_calc_distance_time(self):

        source_lat = '52.632930'
        source_lon = '-1.161572'
        speed = 60
        object = {u'lat': '52.632912', u'lon': '-1.157873', u'road_type': 1, u'time': 0}
        traffic_load = 0
        junc = self.GlobalRoute
        choice = junc.calculate_junction_distance_time(source_lat, source_lon, speed, object, traffic_load)
        print choice
        self.assertTrue(choice, 4.160666920213371)

    def test_pick_random_edge_route(self):
        junc = self.JunctionHandler
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
