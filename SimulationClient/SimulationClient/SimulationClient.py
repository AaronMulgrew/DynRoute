from locust import HttpLocust, TaskSet, task
import json
import time

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print "Starting"
        self.do_traverse()

    def do_traverse(self):
        self.client.verify = False
        response = self.client.get("/")
        print response.content
        content = json.loads(response.content)
        print content
        route = content['route']
        while route != []:
            response = self.client.get('/coordinates/' + route['lat'] + ':' + route['lon'])
            print response.content
            content = json.loads(response.content)
            lat = content['route']['lat']
            lon = content['route']['lon']
            route = content['route']
        print "Finished"


    @task(1)
    def index(self):
        self.client.verify = False
        response = self.client.get("/")
        print response.content
        content = json.loads(response.content)
        print content
        route = content['route']
        while route != []:
            response = self.client.get('/coordinates/' + route['lat'] + ':' + route['lon'])
            print response.content
            content = json.loads(response.content)
            lat = content['route']['lat']
            lon = content['route']['lon']
            route = content['route']
            time.sleep(content['time'])
        print "Finished"

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000