''' This is the base server.py file,
mainly used for endpoint redirection to the models and scripts folders
'''
import json
from flask import (current_app, url_for, \
render_template, redirect, session)
from flask_api import status
from __init__ import (app, bcrypt, request, junction_handler, \
   global_route, add_junction, db, exc)
routehandler = global_route.GlobalRouteHandler()
from scripts import API_auth
import settings
import uuid
from models import emergency_route
from models import login as check_login
from OpenSSL import SSL
from scripts import UserDB
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('certs/domain.crt', 'certs/domain.key')






@app.route('/coordinates/<coordinates>', methods = ['GET'])
def coords(coordinates):
    lat_lon = coordinates.split(":")
    lat = str(lat_lon[0])
    lon = str(lat_lon[1])
    Junction = junction_handler.JunctionHandler([lat,lon])
    routeExists = Junction.check_if_route_exists()
    if isinstance(routeExists, str):
        # this runs if the junctionhandler returns an error
        return routeExists, status.HTTP_400_BAD_REQUEST
    elif routeExists == True:
        route = Junction.generate_route()
        return json.dumps(route)
    else:
        return "Junction Not Found.", status.HTTP_400_BAD_REQUEST

@app.route('/')
def send_homepage():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		print session['username']
		return render_template('index.html', data=session['username'])


@app.route('/calculate_time', methods = ['GET'])
def calc_time():
    coords = json.loads(request.headers['route'])
    result = routehandler.calculate_time_route(coords)
    return json.dumps(result)


@app.route('/config')
def send_config():
    if 'logged_in' in session.keys() and 'admin' in session.keys():
    	return render_template('config.html')
    else:
        return render_template('Unauthorized.html')

@app.route('/add_state', methods= ['POST'])
def add_state():
    state = request.form['state']
    request_data = json.loads(state)
    #state = str(request_data['state'])
    auth_token = str(request.headers['auth_token'])
    checklogin = check_login.check_auth_token(auth_token)
    if checklogin['success']:
        if checklogin['isAdmin']:
            result = routehandler.update_all_routes(request_data)
            return json.dumps(result)
        else:
            return "not Admin"
    return "not Admin"

@app.route("/logout")
def logout():
    """Logout Form"""
    session.pop('auth_token', None)
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('admin', None)

    return redirect(url_for('send_homepage'))


@app.route('/add_junction/', methods=['GET','POST'])
def add_junc_endpoint():
    if request.method == 'GET':
        if 'logged_in' in session.keys() and 'admin' in session.keys():
            routehandler.refresh_all_routes()
            return render_template('add_junction.html')
        else:
            return render_template('Unauthorized.html')
    else:
        if 'logged_in' in session.keys():
            auth_token = session['auth_token']
            # verify that the authorisation token used
            # is valid.
            result = check_login.check_auth_token(auth_token)
            if 'isAdmin' in result:
                request_data = request.get_json()
                add_junc = add_junction.AddJunction()
                add_junc_result = add_junc.add_junction(request_data)
                return json.dumps(add_junc_result)
            else:
                return json.dumps(result['return_value'])

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = str(request.form['username'])
        passw = str(request.form['password'])
        result = check_login.check_login(name, passw)
        if 'password' in result:
            token = API_auth.encode(name, result['password'])
            session['logged_in'] = True
            session['auth_token'] = token
            session['username'] = name
            if 'IsAdmin' in result:
                session['admin'] = True
            return redirect(url_for('send_homepage'))
        else:
            return render_template('login.html', error='Wrong username or password')

@app.route('/login_api', methods=['POST'])
def login_api():
    name = str(request.form['username'])
    passw = str(request.form['password'])
    result = check_login.check_login(name, passw)
    if result == "Wrong":
        return "wrong Username or Password", status.HTTP_401_UNAUTHORIZED
    elif result == "Invalid":
        return "invalid Username or Password", status.HTTP_401_UNAUTHORIZED
    else:
        # generates a token based on the password hash
        token = API_auth.encode(name, result['password'])
        return json.dumps({'token':token})

@app.route('/get_all_usernames', methods=['GET'])
def get_all_usernames():
    if 'logged_in' in session.keys():
        auth_token = session['auth_token']
        # verify that the authorisation token used
        # is valid.
        result = check_login.check_auth_token(auth_token)
        if result['success'] and result['isAdmin']:
            usernames = list()
            users = UserDB.User.query.all()
            for user in users:
                if user.username == 'Admin':
                    pass
                else:
                    usernames.append(user.username)
            return json.dumps(usernames)
        else:
            session.pop('auth_token', None)
            session.pop('logged_in', None)
            session.pop('username', None)
            return "Session token has expired!"
    else:
        return render_template('Unauthorized.html')


@app.route('/all_routes_api')
def return_all_routes_api():
    all_junctions = routehandler.return_all_routes_raw()
    return json.dumps(all_junctions)


@app.route('/add_new_user', methods=['POST'])
def add_new_user():
    request_data = json.loads(request.data)
    name = str(request_data['username'])
    auth_token = str(request_data['auth_token'])
    # check that the auth token is actually valid
    result = check_login.check_auth_token(auth_token)
    if result['success'] and result['isAdmin']:
        password = str(uuid.uuid4())
        newusername = UserDB.User(False, name, password)
        db.session.add(newusername)
        try:
            db.session.commit()
            return json.dumps([True, password])
        except exc.IntegrityError:
            return json.dumps([False, "Username Already Exists."])
    else:
        return json.dumps([False, "Invalid or expired session token."])


@app.route('/generate_user_password', methods=['POST'])
def generate_user_password():
    request_data = json.loads(request.data)
    name = str(request_data['username'])
    auth_token = str(request_data['auth_token'])
    # check that the auth token is actually valid
    result = check_login.check_auth_token(auth_token)
    if result['success'] and result['isAdmin']:
        newpassword = str(uuid.uuid4())
        data = UserDB.User.query.filter_by(username=name).first()
        # this is a threadsafe way of getting the user object
        local_object = db.session.merge(data)
        pwhash = bcrypt.generate_password_hash(newpassword)
        local_object.password = pwhash
        db.session.commit()
        return json.dumps([True, newpassword])
    else:
        return json.dumps([False, "Invalid or expired session token."])

@app.route('/delete_user', methods=['POST'])
def delete_user():
    request_data = json.loads(request.data)
    name = str(request_data['username'])
    auth_token = str(request_data['auth_token'])
    # check that the auth token is actually valid
    result = check_login.check_auth_token(auth_token)
    if result['success'] and result['isAdmin']:
        data = UserDB.User.query.filter_by(username=name).first()
        # this is a threadsafe way of getting the user object
        local_object = db.session.merge(data)
        db.session.delete(local_object)
        db.session.commit()
        return json.dumps([True, ""])
    else:
        return json.dumps([False, "Invalid or expired session token."])


@app.route('/junc_icon<traffic_load>.png')
def send_junc_icon(traffic_load):
    try:
        traffic_load = int(traffic_load)
    except ValueError:
        # this defaults back to the grey traffic load
        traffic_load = 1000
    if traffic_load <= 10:
        filename = 'junc_icon0-10.png'
    elif traffic_load <= 40:
        filename = 'junc_icon11-40.png'
    elif traffic_load <= 75:
        filename = 'junc_icon41-75.png'
    elif traffic_load <= 100:
        filename = 'junc_icon76-100.png'
    else:
        filename = 'junc_icon.png'

    return current_app.send_static_file(str(filename))

@app.route('/all_juncts')
def return_all_junctions():
    all_junctions = routehandler.return_all_junctions()
    return json.dumps(all_junctions)

@app.route('/MovingMarker.js')
def send_javascript():
    return current_app.send_static_file('MovingMarker.js')


@app.route('/generate_emergency')
def generate_emergency_route():
    ## simple check to see if the auth token is in the request 
    ## header
    if 'auth-token' in request.headers:
        ## default back to standard route if not specified in the headers
        lat_lon_list = ['source-lat', 'source-lon', 'dest-lat', 'dest-lon']
        if all (k in request.headers for k in lat_lon_list):
            source_lat = request.headers['source-lat']
            source_lon = request.headers['source-lon']
            dest_lat = request.headers['dest-lat']
            dest_lon = request.headers['dest-lon']
        else:
            source_lat = '52.632930'
            source_lon = '-1.161572'
            dest_lat = '52.637952'
            dest_lon = '-1.123362'
        # this is the end point for the generate emergency token
        auth_token = request.headers['auth-token']
        result = check_login.check_auth_token(auth_token)
        if result['success']:
            junc = junction_handler.JunctionHandler()
            coords_valid_source = junc.check_coords_valid(source_lat, source_lon)
            if coords_valid_source:
                coords_valid_dest = junc.check_coords_valid(dest_lat, dest_lon)
                if coords_valid_dest:
                    Emergency = emergency_route.EmergencyHandler(source_lat, source_lon, dest_lat, dest_lon)
                    route = Emergency.generate_emergency()
                    return_value = json.dumps(route)
                    #response_content = emergency_route.emergency_route(auth_token)
                    #content = response_content[0]
                    return return_value
                else:
                    return "Invalid coordinates", status.HTTP_400_BAD_REQUEST
            else:
                return "Invalid coordinates", status.HTTP_400_BAD_REQUEST
        else:
            return result['return_value'], status.HTTP_401_UNAUTHORIZED
    else:
        return "No auth token", status.HTTP_401_UNAUTHORIZED


@app.route('/gen_route')
def generate_edge_coords():
    junc = junction_handler.JunctionHandler()
    route = junc.generate_route()
    #lat = gen_coord_lat()
    #lon = gen_coord_lon()
    return json.dumps(route)

if __name__ == "__main__":
    app.secret_key = settings.SECRET_KEY
    app.run(debug=False, ssl_context=context)