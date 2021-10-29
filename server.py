# A LAN Chat application with Sockets in Python

import os
import socket
from threading import Thread


# creating the socket object
####################################################################################
s = socket.socket()		# It automatically choses IPv4 and TCP
####################################################################################
HOST = 'localhost'
PORT = 6969

# defining some global variables
####################################################################################
HOST = 'localhost'
PORT = 6969

MAXCONN = 5		# maximum connections to accept

BUFF = 2048		# Max Buffer size

clients = []  # the client list holds all the ip addresses and port numbers of clients connected to the server
names = []		# the names list holds all the nicknames of the clients connected to the server
####################################################################################


# getting the server ready
####################################################################################
# bind host and port
s.bind((HOST, PORT))

# listen for incoming connections
print("[~] Waiting for incoming connections")
s.listen(MAXCONN)
####################################################################################


# broadcast a message to every client but will not be printed on the server
# the server will only monitor the clients
####################################################################################
def broadcast(message, sender, isName):
    for client in clients:
        if client != sender:
            client.send(message)
        # if isName:
        # 	if client != sender:
        # 		client.send(message)
        # else:
        # 	if client != sender:
        # 		client.send(message)

####################################################################################


# handle all client connections
##########################################################################################################
def handle(client):
    while True:
        message = client.recv(BUFF)
        if message:
            if "$name:" in message.decode():
                status = f"$#[+] {message.decode()[7:]} has joined the chat\n".encode()
                broadcast(status, client, 1)
            else:
                broadcast(message, client, 0)

##########################################################################################################


def getName(client):
    client.send("$$".encode())


# recieve info from clients and process them
##########################################################################################################
def receive():
    print("Listening...")
    while True:
        client, addr = s.accept()

        clients.append(client)
        print(f"[+] Client IP = {addr[0]} is connected with PORT = {addr[1]}")

        getName(client)

        thread = Thread(target=handle, args=[client])
        thread.start()

###########################################################################################################


# run the program
receive()
