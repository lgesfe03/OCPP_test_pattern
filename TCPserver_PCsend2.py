# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 08:31:25 2022

@author: Mark
"""

import socket
import time

# Initialize Socket Instance
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
print ("Socket created successfully.")

cnt = 0
# Defining port and host
port = 8765
host = ''

# binding to the host and port
sock.bind((host, port))

# Accepts up to 10 connections
sock.listen(100)
print('Socket is listening...')

while True:
    # Establish connection with the clients.
    con, addr = sock.accept()
    print('Connected with ', addr)
    con.send('send first messeage:'.encode())
    while addr:
        # Get data from the client
        data = con.recv(512)
        print('rx Start :')
        print(data.decode())
        print('============rx And============')
        if ((cnt%2) == 1):
            con.send(('got messeage:'+str(cnt)).encode())
            print('tx: has send......\n')
        cnt += 1
        
        time.sleep(1)
    
# =============================================================================
#     if KeyboardInterrupt:
#         #con.close()
#         print('KeyboardInterrupt & con.close()')
#         continue
# =============================================================================
