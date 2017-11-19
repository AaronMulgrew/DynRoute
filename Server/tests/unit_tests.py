import unittest

from scripts import haversine

class test_haversine(unittest.TestCase):
    def test_haversine(self):
        ## this is the distance from the two sets of coordinates in metres.
        distance = 249.6400152128023
        self.assertEqual(haversine.get_distance_haversine([52.632930, -1.161572], [52.632912, -1.157873]), distance)

if __name__ == '__main__':
    unittest.main()
