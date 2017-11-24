import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
#print sys.path
#test = open("../routes.json", "r").read()
import haversine
import server

class test_haversine(unittest.TestCase):
    def test_haversine(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 249.6400152128023
        self.assertEqual(haversine.get_distance_haversine([52.632930, -1.161572], [52.632912, -1.157873]), distance)

class test_JunctionHandler(unittest.TestCase):
    def test_handler(self):
        newserver = server
        newserver.loadRoutes("../routes.json")
        junc = newserver.JunctionHandler()
        # make sure our junction created is really an instance of the server.junctionhandler
        self.assertTrue(isinstance(junc, server.JunctionHandler))
        print junc

if __name__ == '__main__':
    unittest.main()
