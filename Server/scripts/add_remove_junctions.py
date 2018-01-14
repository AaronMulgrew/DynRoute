import json

junct_data = open("routes.json").read()
parsed = json.loads(junct_data)

def add_junction(lat, lon):
    print "not implemented"



def edit_junction(lat, lon):
    element_to_edit = raw_input("Please type element to edit [speed/junction name]")
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

def del_junction(lat, lon):
    print "not implemented"

def view_junction():
    for element in parsed['junctions']:
        latlon = element.split("//")
        print "Latitude: " + str(latlon[0])
        print "Longitude: " + str(latlon[1])
    junction_lat = raw_input("Please enter a junction Latitude: ")
    junction_lon = raw_input("Please enter a junction Longitude: ")
    #print junction_lat
    #print junction_long
    print parsed['junctions'][junction_lat+'//'+junction_lon]['junction_name']
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