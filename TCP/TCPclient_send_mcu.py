# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 18:47:21 2022

@author: Mark
"""
#----- A simple TCP client program in Python using send() function -----
import socket

# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Connect to the server
clientSocket.connect(("192.168.3.100",502));

# Send data to server
data = "0 1 2 3 4 5 6 7";

clientSocket.send(data.encode());

 

# Receive data from server
dataFromServer = clientSocket.recv(1024);

 

# Print to the console
print(dataFromServer.decode());
indata = clientSocket.recv(1024)
clientSocket.close()
if len(indata) == 0: # connection closed
    clientSocket.close()
    print('server closed connection.')
    
print('recv: ' + indata.decode())