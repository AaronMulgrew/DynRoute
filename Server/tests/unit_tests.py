import unittest
import sys, os
import json
import datetime
import mock
import all_routes
from scripts import haversine
from models import junction_handler, emergency_route, global_route, dijkstra_algorithm, add_junction
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
        server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unit_test.db'
        # creates a test client
        self.app = server.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

        #self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unit_test.db'


    def test_gen_route(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/gen_route')
        assert result.status_code == 200

    def test_gen_route_json(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/gen_route')
        data = json.loads(result.data)
        # make sure that there is a latitude key in the dict
        assert 'lat' in data
        assert 'lon' in data



    def test_login_extreme_min(self):

        result = self.app.post('/login_api', data=dict(
        username='',
        password=''))
        self.assertEqual(result.data, "invalid Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_min(self):
        result = self.app.post('/login_api', data=dict(
        username='A',
        password='1'))
        self.assertEqual(result.data, "wrong Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_min_plus_one(self):
        result = self.app.post('/login_api', data=dict(
        username='Ad',
        password='12'))
        self.assertEqual(result.data, "wrong Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_max_minus_one(self):
        result = self.app.post('/login_api', data=dict(
        username='1234567893123212131231232122223323213213213321332',
        password='1234567893123212131231232122223323213213213321332'))
        self.assertEqual(result.data, "wrong Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_max(self):
        result = self.app.post('/login_api', data=dict(
        username='12345678931232121312312321222233232132132133213321',
        password='12345678931232121312312321222233232132132133213321'))
        self.assertEqual(result.data, "wrong Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_max_plus_one(self):
        result = self.app.post('/login_api', data=dict(
        username='123456789312321213123123212222332321321321332133212',
        password='123456789312321213123123212222332321321321332133212'))
        self.assertEqual(result.data, "invalid Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_mid(self):
        result = self.app.post('/login_api', data=dict(
        username='Admin',
        password='123456'))
        data = json.loads(result.data)
        assert 'token' in data

    def test_login_extreme_max(self):
        result = self.app.post('/login_api', data=dict(
        username='123456789312321213123123212222332321321321332133212123456789312321213123123212222332321321321332133212',
        password='123456789312321213123123212222332321321321332133212123456789312321213123123212222332321321321332133212'))
        self.assertEqual(result.data, "invalid Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_login_invalid(self):
        result = self.app.post('/login_api', data=dict(
        username="DROP TABLE USER;",
        password="SELECT * FROM USER"))
        self.assertEqual(result.data, "wrong Username or Password")
        self.assertEqual(result.status_code, 401)

    def test_gen_next_route(self):
        result = self.app.get('coordinates/52.632912:-1.157873')
        assert result.status_code == 200


    def test_gen_next_route_extreme_min(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/-8888:-12000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Invalid data format")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_min_minus_one(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/-91.000:-181.000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Invalid data format")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_min(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/-90.000:-180.000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Junction Not Found.")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_min_plus_one(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/-79:000:-179.000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Junction Not Found.")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_max_minus_one(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/+79.000:179.000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Junction Not Found.")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_max(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/+80.000:180.000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Junction Not Found.")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_max_plus_one(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/+81.000:181.000')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Invalid data format")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_mid(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/52.632912:-1.157873')
        data = json.loads(result.data)
        # make sure that there is a latitude key in the dict
        assert 'lat' in data
        assert 'lon' in data

    def test_gen_next_route_extreme_max(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/32109382:312397812')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Invalid data format")
        self.assertEqual(result.status_code, 400)


    def test_gen_next_route_invalid_data_type(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/Ejejeje:eqweqw')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Invalid data format")
        self.assertEqual(result.status_code, 400)

    def test_gen_next_route_invalid_data_type_2(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('coordinates/--2333:+++3333')
        data = result.data
        # make sure that there is a latitude key in the dict
        self.assertEqual(data,"Invalid data format")
        self.assertEqual(result.status_code, 400)


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

class test_add_junction(unittest.TestCase):

    def test_process_lat_lon_float(self):
        addJunction = add_junction.AddJunction()
        result = addJunction.process_lat_lon_float('123123.12331324242424')
        print result
        self.assertEqual(result, '123123.123313')

    def test_add_junction(self):
        # this function mocks the add junction function
        # to ensure that the data isn't added to the routes.json file.
        addJunction = add_junction.AddJunction()
        addJunction.add_to_json = mock.Mock(return_value=True)
        request = {'JuncName': 'ABC', 'NewLatLon': '52.63733423683968//42.476863538',\
           'OldLatLon': '52.634169//-1.149998', 'RoadType': '2',\
          'SelectedJunction': 'A47 - Glenfield Road East', 'Speed': '20'}
        result = addJunction.add_junction(request)
        self.assertEqual(result, True)


    def test_search_by_route_name(self):
        addJunction = add_junction.AddJunction()
        addJunction.write_to_file = mock.Mock(return_value=True)
        request = {'JuncName': 'ABC', 'NewLatLon': '52.63733423683968//42.476863538', 'OldLatLon': '52.634169//-1.149998', 'RoadType': '2', 'SelectedJunction': 'A47 - Glenfield Road East', 'Speed': '20'}
        result = addJunction.add_junction(request)
        self.assertEqual(result, True)
        if (result):
            result = addJunction.search_by_route_name()
            self.assertEqual(result, True)


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
        route_lat = "111"
        route_lon = "222"

        traffic_load = 24
        returnvar = self.allroutes.update_traffic_load(coords, route_lat, route_lon, traffic_load)
        self.assertFalse(returnvar)

class test_emergency_handler(unittest.TestCase):
    def test_emergency(self):
        emergency = emergency_route.EmergencyHandler("-122", "-8", "-1", "-5")
        result = emergency.generate_emergency()
        self.assertIsNotNone(result)

class test_emergency_handler_endpoint(unittest.TestCase):

    def setUp(self):

        server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unit_test.db'
        # creates a test client
        self.app = server.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        result = self.app.post('/login_api', data={"username":"Admin", "password":"123456"})
        data = json.loads(result.data)
        token = data['token']
        self.token = token

    def test_emergency_extreme_min(self):

        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"-8888", "source-lat":"-12000", "dest-lat": "-12000", "dest-lon": "-8888"})
        self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 400)
        #result = self.app.get('/login_api', headers=dict(
        #source-lon='-8888',
        #source-lat='-12000',
        #dest-lat = '-12000',
        #dest-lon = '-8888'))

    def test_emergency_min_minus_one(self):
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"-181.000", "source-lat":"-91.000", "dest-lat": "91.000", "dest-lon": "-181.000"})
        #self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 400)

    def test_emergency_min(self):
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"-180.000", "source-lat":"-90.000", "dest-lat": "90.000", "dest-lon": "-180.000"})
        self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        #self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 200)

    def test_emergency_min_plus_one(self):
        #{"source-lon":"-179.000", "source-lat":"-89.000", "dest-lat": "89.000", "dest-lon": "-179.000"}
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"-179.000", "source-lat":"-89.000", "dest-lat": "89.000", "dest-lon": "-179.000"})
        self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        #self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 200)

    def test_emergency_max_minus_one(self):
        #{"source-lon":"+179.000", "source-lat":"+89.000", "dest-lat": "-89.000", "dest-lon": "+179.000"}
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"+179.000", "source-lat":"+89.000", "dest-lat": "-89.000", "dest-lon": "+179.000"})
        self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        #self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 200)

    def test_emergency_max(self):
        #{"source-lon":"+179.000", "source-lat":"+89.000", "dest-lat": "-89.000", "dest-lon": "+179.000"}
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"+180.000", "source-lat":"+90.000", "dest-lat": "-90.000", "dest-lon": "+180.000"})
        self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        #self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 200)

    def test_emergency_max_plus_one(self):
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"-181.000", "source-lat":"-91.000", "dest-lat": "91.000", "dest-lon": "-181.000"})
        #self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 400)

    def test_emergency_extreme_max(self):
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":" -12161572","source-lat":"5231632930", "dest-lon":" -133137.921","dest-lat":" 5336385.12"})
        #self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 400)

    def test_emergency_invalid_1(self):
        #{"source-lon":"dkdkdk","source-lat"-"edueih", "dest-lon":"djdjdjd","dest-lat":" deioude"}
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"dkdkdk","source-lat":"edueih", "dest-lon":"djdjdjd","dest-lat":" deioude"})
        #self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 400)

    def test_emergency_invalid_2(self):
        result = self.app.get('/generate_emergency', headers={"auth-token":self.token, "source-lon":"-229292","source-lat":"+++++2828228", "dest-lon":"--23424","dest-lat":"++2342443"})
        #self.assertEqual(json.loads(result.data), {"route":[], "time":0})
        self.assertEqual(result.data, "Invalid coordinates")
        self.assertEqual(result.status_code, 400)

class test_haversine(unittest.TestCase):
    def test_haversine(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 249.6400152128023
        self.assertEqual(haversine.get_distance_haversine([52.632930, -1.161572, 52.632912, -1.157873]), distance)

    def test_haversine_min(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 1.1119492664455877
        lat1 = 0.00000
        lon1 = 0.00000
        lat2 = 0.00000
        lon2 = 0.00001
        self.assertEqual(haversine.get_distance_haversine([lat1, lon1, lat2, lon2]), distance)

    def test_haversine_max(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 10007543.398010286
        lat1 = 0.00000
        lon1 = 0.00000
        lat2 = 90
        lon2 = -180
        x = haversine.get_distance_haversine([lat1, lon1, lat2, lon2])
        self.assertEqual(haversine.get_distance_haversine([lat1, lon1, lat2, lon2]), distance)

    def test_haversine_invalid(self):
        lat1 = "zzzzz"
        lon1 = "xxxxx"
        lat2 = 90
        lon2 = -180
        # this test checks that the Exception that is raised
        # also matches with the error message.
        self.assertRaisesRegexp(TypeError, "Could not convert as variables are not floats", haversine.get_distance_haversine, [lat1, lon1, lat2, lon2])

class test_dijkstra(unittest.TestCase):

    def test_dijkstra_algorithm_basic(self):
        dijkstra = dijkstra_algorithm.Dijkstra()
        edges = {
	    "A-B": [{
		    "dest": "B",
		    "source": "A",
		    "time": 3.3231189058838946
	    }],
	    "A-C": [{
		    "dest": "C",
		    "source": "A",
		    "time": 1
	    }],
	    "C-D": [{
		    "dest": "D",
		    "source": "C",
		    "time": 7
	    }],	
        "B-D": [{
		    "dest": "D",
		    "source": "B",
		    "time": 3
	    }]}
        dijkstra.set_edges(edges)
        result = dijkstra.compute_shortest_route("A", "D")
        self.assertEqual(result['route'], ["B", "D"])


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
