from pymongo import MongoClient
from bson.objectid import ObjectId

cluster = MongoClient('mongodb+srv://hazemhamdy389:chwAYJALG3x3kPos@cluster0.ysiuago.mongodb.net/',
                      tls=True,  # Enable SSL/TLS
    tlsAllowInvalidCertificates=True,  # Allow invalid SSL certificates for debugging
    serverSelectionTimeoutMS=10000)
database = cluster["p2p-chat"]
# password = "chwAYJALG3x3kPos"

# Includes database operations
class DB:


    # db initializations
    # def __init__(self):
    #     self.client = MongoClient('mongodb://localhost:27017/')
    #     self.db = self.client['p2p-chat']


    # checks if an account with the username exists
    def is_account_exist(self,username):
        if database.accounts.find_one({'username': username}):
            return True
        else:
            return False
    
    def get_all_users(self):
        return list(database.accounts.find({},{'username':1,'_id':0}).sort("username", 1))
    
    def get_all_online_peers(self):
        return list(database.online_peers.find({},{'_id':0}).sort('username',1))

    
    # registers a user
    def register(self, username, password):
        if database.accounts.find_one({'username': username}):
          print("this username is already in use")
          return False
        else :
          account = {
            "username": username,
            "password": password,
            "rooms" : []

          }
          database.accounts.insert_one(account)
          return True


    # retrieves the password for a given username
    def get_password(self, username):
        return database.accounts.find_one({"username": username})["password"]


    # checks if an account with the username online
    def is_account_online(self, username):
        onlinePeer = database.online_peers.find_one({"username": username},{"_id":0})
        print(onlinePeer['ip'])
        return (onlinePeer["ip"], onlinePeer["port"])

    
    # logs in the user
    def user_login(self,username,password, ip, port):
        account = database.accounts.find_one({"username" : username,"password" : password})
        if account is not None:
          online_peer = {
            "username": username,
            "ip": ip,
            "port": port
          }
          database.online_peers.insert_one(online_peer)
          return True
        else:
            print("Wrong Credentials")
            return False
            
    

    # logs out the user 
    def user_logout(self, username):
        database.online_peers.delete_one({"username": username})
        return True
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = database.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    def create_room(self, name,users):
        if database.rooms.find({'name': name}) is None:
           room = database.rooms.insert_one({
             "name" : name,
             "users" : users
            })
           database.accounts.update_many({'username' : {'$in' : users}},{'$push' : {'rooms' : {'name':name}}})
           return True
        else: 
            return False

    def add_user_to_room(self, roomName,newUsername):
        res = database.accounts.find_one({'username':newUsername})

        if res is not None:
           database.rooms.update_one({'name' : roomName},{'$addToSet' : {'users' : newUsername}})
           database.accounts.update_one({'username' : newUsername},{'$addToSet' : {'rooms' : {'name':roomName}}})
           return True
        else:
            print("User Not Found")
            return False
        
    def remove_user_from_room(self, roomName,newUsername):
           database.rooms.update_one({'name' : roomName},{'$pull' : {'users' : newUsername}})
           database.accounts.update_one({'username' : newUsername},{'$pull' : {'rooms' : {'name':roomName}}})
           return True
        
    def get_user_rooms(self, username):
       res = database.accounts.find_one({'username' : username},{"rooms":1})
       return res['rooms']

    def get_room_online_accounts(self, roomName):
        users = database.rooms.find_one({'name':roomName},{'users' : 1})['users']
       # print(users)
        online_users = database.online_peers.find({'username' : {'$in' : users}},{'username' : 1,'ip' : 1,'port' : 1,'_id':0})
        return list(online_users)
    

