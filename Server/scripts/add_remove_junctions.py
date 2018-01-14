import json
from collections import defaultdict

junct_data = open("routes.json").read()
parsed = json.loads(junct_data)

def add_junction():
    lat = raw_input("Please type latitude of intended junction: ")
    lon = raw_input("Please type longitude of intended junction: ")
    junc_name = raw_input("Please type name of junction: ")
    speed = raw_input("Please type speed of junction: ")
    routes_amount = raw_input("Please type how many routes are available from the junction: ")
    routes_amount = int(routes_amount)
    routes = list()
    for i in xrange(routes_amount):
        dictionary = {}
        dictionary['lat'] = raw_input("Please type the latitude of route: ")
        dictionary['lon'] = raw_input("Please type longitude of route: ")
        dictionary['road_type'] = raw_input("Please type road type of route: ")
        routes.append(dictionary)
    parsed['junctions'][lat+'//'+lon] = {}
    parsed['junctions'][lat+'//'+lon]['junc_name'] = junc_name
    parsed['junctions'][lat+'//'+lon]['speed'] = speed
    parsed['junctions'][lat+'//'+lon]['routes'] = routes




def edit_junction(lat, lon):
    element_to_edit = raw_input("Please type element to edit [speed/junction name/routes]")
    if element_to_edit.upper() == "SPEED":
        current_element = parsed['junctions'][lat+'//'+lon]['speed']
        new_val = raw_input("Current Speed is" + str(current_element) + "\n New speed: ")
        try:
            new_val = int(new_val)
            print "New speed is: " + str(new_val)
            parsed['junctions'][lat+'//'+lon]['speed'] = new_val
        except Exception as e:
            print e
        print (parsed['junctions'][lat+'//'+lon]['speed'])
    elif element_to_edit.upper() == "JUNCTION NAME":
        current_element = parsed['junctions'][lat + '//' + lon]['junction_name']
        new_val = raw_input("Current Junction name is: " + str(current_element) + "\n new Name: ")
        parsed['junctions'][lat+'//'+lon]['junction_name'] = new_val
    elif element_to_edit.upper() == 'ROUTES':
        print "Current Routes: "
        current_element = parsed['junctions'][lat+'//'+lon]['routes']
        for element in current_element:
            print element

def del_junction(lat, lon):
    print "not implemented"

def view_junction():
    for element in parsed['junctions']:
        latlon = element.split("//")
        print "Latitude: " + str(latlon[0])
        print "Longitude: " + str(latlon[1])
        print "Junction name: " + str(parsed['junctions'][element]['junction_name'])
        print "\n ----------------------------------------------------- \n"
    junction_lat = raw_input("Please enter a junction Latitude: ")
    junction_lon = raw_input("Please enter a junction Longitude: ")
    #print junction_lat
    #print junction_long
    try:
        print parsed['junctions'][junction_lat+'//'+junction_lon]['junction_name']
    except KeyError:
        print "Unfortunately your request did not return any results."
        view_junction()
    usr_input = raw_input("Would you like to edit or delete this junction? [E/D]")
    if usr_input.upper() == 'E':
        edit_junction(junction_lat, junction_lon)
    elif usr_input.upper() == 'D':
        del_junction(junction_lat, junction_lon)
    else:
        print "Please type either E or D."
        view_junction()
    

#junct_data = open("routes.json").read()
#parsed = json.loads(junct_data)
#for element in parsed['junctions']:
#    print element

def start():
    usr_input = raw_input("Would you like to view, add or delete a junction? [V, A, D]")
    if usr_input.upper() == 'V':
        print 'v'
        view_junction()
    elif usr_input.upper() == 'A':
        print 'a'
        add_junction()
    elif usr_input.upper() == 'D':
        print 'd'
        del_junction()
    usr_input = raw_input("Would you like to continue? [Y, N]")
    if usr_input.upper() == 'Y':
        start()
    else:
        with open('routes.json', 'w') as outfile:
            json.dump(parsed, outfile)
        exit(0)

if __name__ == "__main__":
    start()
#print json.dumps(parsed, indent=4, sort_keys=True)