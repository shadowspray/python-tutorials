# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Echo client program
import socket

HOST = ''    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print 'Send data from client'
s.sendall('Hello, world!')
print 'Receive data from server'
data = s.recv(1024)
print 'Close connection'
s.close()
print 'Received', repr(data)
