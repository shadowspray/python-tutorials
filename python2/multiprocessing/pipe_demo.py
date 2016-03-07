# -*- coding: utf-8 -*-
import os
import random

from multiprocessing import Process, Pipe


def producer_task(conn):
    print 'start producer task'
    for i in xrange(10):
        value = random.randint(1, 100)
        conn.send(value)
        print('Value [%d] sent by PID [%d]' % (value, os.getpid()))
    conn.close()


def consumer_task(conn):
    print 'start consumer task'
    while conn.poll(1):
        print('Value [%d] received by PID [%d]' % (conn.recv(), os.getpid()))
    else:
        print('No more data to receive')


if __name__ == '__main__':
    producer_conn, consumer_conn = Pipe()
    consumer = Process(target=consumer_task, args=(consumer_conn,))
    producer = Process(target=producer_task, args=(producer_conn,))
    consumer.start()
    producer.start()
    consumer.join()
    producer.join()
