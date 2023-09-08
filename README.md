# p2p_chat

## Introduction
In this project, you will learn how P2P applications work and some of their basic functionalities.
Your task is to extend the provided P2P chat program (found on the LMS and at the end of this
document), adding a new feature which is Chat Rooms
A chat room is a group chatting feature where a user can create a room with a room_id, add users to
it.
## Detailed Requirements
### Registry Server
The server is to be extended keeps track of the chat rooms available, and the clients in each room.
Each P2P client must regularly contact the room server to maintain the connection established
initially (client must ping server every 20s to stay alive, or client will be disconnected).
### Client
Each client is extended to acts as both a server (to other P2P clients for distributing messages along
the network), and a client (receiver of messages from other P2P clients). Once a client is registered
on the room at the server, it starts to look for a peer in the chat room it is in currently. When a message
is sent by a user, it must be delivered to all the online participants in the same room.
The message should be marked with a text before displaying the message on the peer screen as
“Message from [USER] at [room_id]: text of the message”.
The user is prompted if it would like to send a message for a peer or to one of its rooms.

## How To use
- Run the registry file first
- run the peer file
- Enter the registry's Ip address
- Create a user
- Login and choose a port, make sure the port isn't already in use
- Create a room
- connect to this room
make sure to not close the registry app or the client app before logging out or it'll create a conflict in the database

##Dependencies
you need to have the following libraries installed
- socket
- threading
- time
- select
- logging
- json
- os
- pymongo
also make sure you have mongoDB and correctly connect to your database
