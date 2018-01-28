import json

class AllRoutes:
    all_routes = json.loads(open("routes.json", "r").read())
    junction_data = dict()