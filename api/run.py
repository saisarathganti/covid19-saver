from flask import Flask, jsonify, request, json
from models import User
from py2neo import Graph, Node
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, decode_token
import re

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

jwt = JWTManager(app)

CORS(app)

@app.route('/users/register', methods=['POST'])
def register():
    username = request.get_json()['email']
    password = request.get_json()['password']
    country = request.get_json()['country']
    created = datetime.utcnow()

    if not re.search(regex,username):
        result = jsonify({'error': 'Invalid email format.'})
    elif not User(username).register(password, country):
        result = jsonify({'error': 'A user with that username already exists.'})
    else:
        result = {
        'email': username,
        'password': password,
        'country': country,
        'created': created
        }
        result = jsonify({'result': result})

    return result

@app.route('/users/location', methods=['POST'])
def add_visited_place():
    latitude = request.get_json()['latitude']
    longitude = request.get_json()['longitude']
    usertoken = request.get_json()['usertoken']
    username = decode_token(usertoken, allow_expired=False).get('identity').get('email')
    created = datetime.utcnow()
    coronaInfected = User(username).add_visited_place(latitude, longitude)
    country = User(username).get_country()
    if not coronaInfected:
        result = jsonify({'error': 'Invalid usertoken'})
    else:
        result = {
        'username': username,
        'latitude': latitude,
        'longitude': longitude,
        'coronaInfected': coronaInfected,
        'country': country,
        'created': created
        }
        result = jsonify({'result': result})

    return result

@app.route('/users/checkLocation', methods=['POST'])
def checkLocation():
    latitude = request.get_json()['latitude']
    longitude = request.get_json()['longitude']
    usertoken = request.get_json()['usertoken']
    username = decode_token(usertoken, allow_expired=False).get('identity').get('email')
    created = datetime.utcnow()
    
    result = list(User(username).check_location(float(latitude), float(longitude)))
    if not result:
        result = jsonify({'error': 'Invalid usertoken'})
    else:
        result = jsonify(result[0]['result'])

    return result

@app.route('/users/updateCoronaInfectedStatus', methods=['POST'])
def updateCoronaInfectedStatus():
    coronaInfected = request.get_json()['coronaInfected']
    usertoken = request.get_json()['usertoken']
    username = decode_token(usertoken, allow_expired=False).get('identity').get('email')
    created = datetime.utcnow()
    
    if not User(username).update_corona_infected_status(coronaInfected):
        result = jsonify({'error': 'Invalid usertoken'})
    else:
        result = {
        'username': username,
        'coronaInfected': coronaInfected,
        'created': created
        }
        result = jsonify({'result': result})

    return result

@app.route('/users/getCoronaInfectedUsersWithDistance', methods=['POST'])
def getCoronaInfectedUsersWithDistance():
    usertoken = request.get_json()['usertoken']
    distance = request.get_json()['distance']
    username = decode_token(usertoken, allow_expired=False).get('identity').get('email')
    created = datetime.utcnow()
    result = list(User(username).get_corona_infected_users_with_distance(int(distance)))
    if not result:
        result = jsonify({'error': 'Invalid usertoken'})
    else:
        result = jsonify(result[0]['result'])
    return result

@app.route('/users/getCoronaInfectedUsersYouExposedTo', methods=['POST'])
def getCoronaInfectedUsersYouExposedTo():
    usertoken = request.get_json()['usertoken']
    username = decode_token(usertoken, allow_expired=False).get('identity').get('email')
    created = datetime.utcnow()
    result = list(User(username).get_corona_infected_users_you_exposed_to())
    if not result:
        result = jsonify({'error': 'Invalid usertoken'})
    else:
        result = jsonify(result[0]['result'])
    return result

@app.route('/users/dashboardlogin', methods=['POST'])
def dashboardlogin():
    password = request.get_json()['password']
    usertoken = request.get_json()['usertoken']
    username = decode_token(usertoken, allow_expired=False).get('identity').get('email')
    
    if not User(username).dashboard_verify_password(password):
        result = jsonify({'error': 'Invalid password'})
    else:
        result = {
        'username': username,
        }
        result = jsonify({'result': result})

    return result

@app.route('/users/login', methods=['POST'])
def login():
    username = request.get_json()['email']
    password = request.get_json()['password']
    result = ""
    if not User(username).verify_password(password):
        result = jsonify({"error": "Invalid username or password"})
    else:
        access_token = create_access_token(
        identity={
            'email': username
        }, expires_delta=False)
        result = jsonify({'result': access_token})

    return result


if __name__ == '__main__':
    app.run(debug=True)
