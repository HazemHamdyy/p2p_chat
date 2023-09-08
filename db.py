from pymongo import MongoClient
from bson import json_util
import os
from dotenv import load_dotenv



# Includes database operations
class DB:


    # db initializations 
    def __init__(self):
        load_dotenv() # Load the .env file
        MONGODB = os.getenv('MONGODB')
        self.client = MongoClient((MONGODB), tls=True,  # Enable SSL/TLS
        tlsAllowInvalidCertificates=True,  # Allow invalid SSL certificates for debugging
        serverSelectionTimeoutMS=10000)
        self.db = self.client['p2p-chat']



    # checks if an account with the username exists
    def is_account_exist(self, username):
        if self.db.accounts.find_one({'username': username}):
            return True
        else:
            return False
    

    # registers a user
    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)


    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]


    # checks if an account with the username online
    def is_account_online(self, username):
        if self.db.online_peers.find_one({"username": username}):
            return True
        else:
            return False

    
    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)
    

    # logs out the user 
    def user_logout(self, username):
        acc=self.db["online_peers"].find_one({"username": username})
        self.db["online_peers"].delete_one(acc)
          # use $pull to remove username from online_peers array in rooms collection
        self.db["rooms"].update_many(
        { "online_peers": username },
        { "$pull": { "online_peers": username } }
        )
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    def create_room(self, name):
        if "rooms" not in self.db.list_collection_names():
            # the room collection does not exist, create it
            room_collection = self.db.create_collection("rooms")
        else:
            # the room collection exists, get it
            room_collection = self.db["rooms"]
        # check if a room with this name already exists
        if room_collection.find_one({"name": name}) is None:
            # the room does not exist, create it
            room = room_collection.insert_one({
            "name" : name,
            "online_peers" : []
            })
            return True
        else: 
            # the room exists, return False
            return False



        
    def get_all_rooms(self):
        rooms = self.db.rooms.find()
        print(rooms)

    def connect_to_room(self,roomName,userName):
        if  self.db.rooms.find_one({'name': roomName}) is None:
            return False
        else:
            # Only push the userName if it is not already in the online_peers array
            self.db.rooms.find_one_and_update({'name': roomName, 'online_peers': {'$nin': [userName]}},{"$push": {
              "online_peers":userName }})
            room =  self.db.rooms.find_one({'name': roomName})
            onlinePeers = room.get("online_peers")
            onlinePeers = self.db.online_peers.find({"username" : {"$in" : onlinePeers}}, {"_id":0})
            onlinePeersList= list(onlinePeers)
            
            return  onlinePeersList
