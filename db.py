from pymongo import MongoClient

# Includes database operations
class DB:


    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb+srv://hazemhamdy389:chwAYJALG3x3kPos@cluster0.ysiuago.mongodb.net/',
                      tls=True,  # Enable SSL/TLS
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
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    def create_room(self, name):
        if  self.db.rooms.find({'name': name}) is None:
           room = self.db.rooms.insert_one({
             "name" : name,
             "online_peers" : []
            })
           return True
        else: 
          return False
        
    def get_all_rooms(self):
        rooms = self.db.rooms.find()
        print(rooms)

    def connect_to_room(self,roomName,userName):
        if  self.db.rooms.find_one({'name': roomName}) is None:
            return False
        else:
            self.db.rooms.find_one_and_update({'name': roomName},{"$push": {
              "online_peers":userName }})
            room =  self.db.rooms.find_one({'name': roomName})
            onlinePeers = room.get("online_peers")
            onlinePeers= list(self.db.online_peers.find({"username" : {"$in" : onlinePeers}},{"_id":0}))
            
            print(onlinePeers)
            return  onlinePeers