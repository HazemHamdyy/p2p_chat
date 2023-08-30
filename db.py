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
    def is_account_exist(username):
        if database.accounts.find_one({'username': username}):
            return True
        else:
            return False
    
    def get_all_users():
        return list(database.accounts.find({},{'username':1,'_id':0}).sort("username", 1))
    
    def get_all_online_peers():
        return list(database.online_peers.find({},{'_id':0}).sort('username',1))

    
    # registers a user
    def register(username, password):
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
    def get_password(username):
        return database.accounts.find_one({"username": username})["password"]


    # checks if an account with the username online
    def is_account_online(username):
        return database.online_peers.find_one({"username": username},{"_id":0})

    
    # logs in the user
    def user_login(username,password, ip, port):
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
            return False
            print("Wrong Credentials")
    

    # logs out the user 
    def user_logout(username):
        database.online_peers.delete_one({"username": username})
        return True
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(username):
        res = database.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    def create_room(name,users):
        room = database.rooms.insert_one({
          "name" : name,
          "users" : users
        })
        database.accounts.update_many({'username' : {'$in' : users}},{'$push' : {'rooms' : {'id' : room.inserted_id,'name':name}}})
        return True

    def add_user_to_room(roomid,roomName,newUsername):
        res = database.accounts.find_one({'username':newUsername})

        if res is not None:
           database.rooms.update_one({'_id' : ObjectId(roomid)},{'$addToSet' : {'users' : newUsername}})
           database.accounts.update_one({'username' : newUsername},{'$addToSet' : {'rooms' : {'id' : roomid,'name':roomName}}})
           return True
        else:
            print("User Not Found")
            return False
        
    def remove_user_from_room(roomid,roomName,newUsername):
           database.rooms.update_one({'_id' : ObjectId(roomid)},{'$pull' : {'users' : newUsername}})
           database.accounts.update_one({'username' : newUsername},{'$pull' : {'rooms' : {'id' : roomid,'name':roomName}}})
           return True
        
    def get_user_rooms(username):
       res = database.accounts.find_one({'username' : username},{"rooms":1})
       return res['rooms']

    def get_room_online_accounts(roomid):
        users = database.rooms.find_one({'_id' : ObjectId(roomid)},{'users' : 1})['users']
       # print(users)
        online_users = database.online_peers.find({'username' : {'$in' : users}},{'username' : 1,'ip' : 1,'port' : 1,'_id':0})
        return list(online_users)
    

