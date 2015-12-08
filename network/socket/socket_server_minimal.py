# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print 'Waiting for client'
s.listen(1) # maximum number of queued connections = 1
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data:
        print "No more data to receive"
        break
    conn.send(data)
conn.close()
