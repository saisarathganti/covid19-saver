from py2neo import Graph, Node, NodeMatcher
from passlib.hash import pbkdf2_sha256
import os
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url + '/db/data/', username='neo4j', password='H96tp@XNTFb48GB')
matcher = NodeMatcher(graph)


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = matcher.match('User', username= self.username).first()
        return user

    def get_country(self):
        user = self.find()
        return user.get('country')

    def register(self, password, country):
        if not self.find():
            user = Node('User',
                username=self.username, 
                password=pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16), 
                country=country,
                coronaInfected='NO'
            )
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user is not None:
            return pbkdf2_sha256.verify(password, user.get('password'))
        else:
            return False

    def dashboard_verify_password(self, password):
        user = self.find()
        if user is not None:
            return password=='tribes-covid-fighter'
        else:
            return False

    def add_visited_place(self, latitude, longitude):
        if not self.find():
            return False
        locationId=str(uuid.uuid4())
        query = '''        
        MATCH (user:User)
        WHERE user.username = {username}
        SET user.currentLocationId = {currentLocationId} 
        WITH user
        CREATE (location:location {id: {locationId}, lat: {latitude}, lon: {longitude}, created: datetime()})<-[:VISITED]-(user)
        '''
        graph.run(query, username=self.username, currentLocationId=locationId, locationId=locationId, latitude=latitude, longitude=longitude)
        return self.find().get('coronaInfected')

    def update_corona_infected_status(self, coronaInfected):
        if not self.find():
            return False
        user = self.find()
        query = '''
        MATCH (user:User)
        WHERE user.username = {username}
        SET user.coronaInfected = {coronaInfected} 
        RETURN user
        '''
        return graph.run(query, username=self.username, coronaInfected=coronaInfected)

    def get_corona_infected_users_with_distance(self, distance):
        if not self.find():
            return False
        user = self.find()
        currentLocationId=user.get('currentLocationId')
        query = '''
        MATCH (currentLocationNode:location)
        WHERE currentLocationNode.id = {currentLocationId}
        WITH currentLocationNode
        match (user: User),(otherLocationNodes: location)
        where user.currentLocationId=otherLocationNodes.id
        with otherLocationNodes, currentLocationNode
        MATCH (otherLocationNodes)
        WHERE distance(point({ longitude: currentLocationNode.lon, latitude: currentLocationNode.lat }) , point({ longitude: otherLocationNodes.lon, latitude: otherLocationNodes.lat })) <{distance}
        WITH otherLocationNodes
        MATCH (otherLocationNodes)<-[:VISITED]-(user:User)
        WHERE user.coronaInfected='YES'
        RETURN collect(user.username) as result
        '''
        return graph.run(query, currentLocationId=currentLocationId, distance=distance)

    def get_corona_infected_users_you_exposed_to(self):
        if not self.find():
            return False
        user = self.find()
        query = '''
        MATCH (user: User)-[:VISITED]->(otherLocationNodes: location)
        WHERE user.username = {username}
        WITH otherLocationNodes
        MATCH (currentLocationNode: location)
        WHERE distance(point({ longitude: currentLocationNode.lon, latitude: currentLocationNode.lat }) , point({ longitude: otherLocationNodes.lon, latitude: otherLocationNodes.lat })) = 0
        WITH DISTINCT currentLocationNode
        MATCH (currentLocationNode)<-[:VISITED]-(user: User)
        WHERE user.coronaInfected='YES'
        RETURN collect(distinct user.username) as result
        '''
        return graph.run(query, username=user.get('username'))

    def check_location(self, latitude, longitude):
        if not self.find():
            return False
        query = '''
        MATCH (loc: location)
        WHERE loc.lat = {latitude} AND loc.lon = {longitude} AND loc.created>=(datetime()-duration({hours: 4}))
        WITH loc
        MATCH (loc)<-[:VISITED]-(user: User)
        RETURN collect(distinct user.username) as result
        '''
        return graph.run(query, latitude=latitude, longitude=longitude)
