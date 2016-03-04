# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import sys
import time

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
print 'Socket Created'

host = 'www.amazon.com'
port = 80

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

s.connect((remote_ip , port))
print 'Socket Connected to', host, 'on ip', remote_ip

message = "GET / HTTP/1.1\r\n\r\n"
try:
    s.sendall(message)
except socket.error:
    print 'Send failed'
    sys.exit()
print 'Message send successfully'


def recv_size(s, size):
    """
    Receive only specified size of data

    :param s: Socket object
    :param size: Size of data in integer
    :return: None
    """
    print 'Receive data in fixed size mode'
    reply = s.recv(size)
    print reply


def recv_timeout(s, timeout=2):
    """
    Receive data within time range

    :param s: Socket object
    :param timeout: Timeout in seconds
    :return: None
    """
    print 'Receive data in timeout mode'
    s.setblocking(0) # Non-blocking

    total_data = []
    data = ''

    begin = time.time()

    while 1:
        if total_data and time.time() - begin > timeout:
            break

        elif time.time() - begin > timeout:
            break

        try:
            data = s.recv(128)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except Exception as e:
            # print 'Error:', e
            pass

    print ''.join(total_data)


MODE_FIXED_SIZE = 1
MODE_TIMEOUT = 2

mode = MODE_TIMEOUT

if mode == MODE_FIXED_SIZE:
    # Note that received data is incomplete
    recv_size(s, 128)
elif mode == MODE_TIMEOUT:
    # Note that received data is now complete
    recv_timeout(s)
