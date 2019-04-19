# IN CAR
# This will be server
import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import requests,json
import time
import threading
# Get the ip
def get_ip():
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        except Exception as e:
            print('cant get ip:{}'.format(e))
            time.sleep(5)
            get_ip()
# Host
HOST = get_ip()
# Port
PORT = 8082
#  conn array  ( your client )
all_connections = []
def start_streaming():
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret,frame = cap.read()
            data = pickle.dumps(frame)
            for conn in all_connections:
                try:
                    conn.sendall(struct.pack("L", len(data)) + data)
                except Exception as e:
                    test_line()
##            cv2.imshow('windows',frame)
##            cv2.waitKey(10)
    except Exception as e:
        print(e)
# check if the client still online
def test_line():
    for conn in all_connections:
        try:
            conn.sendall('t')
        except Exception as e:
            all_connections.remove(conn)
# create a socket
def create_continue_server():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print('created a server')
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            print('\nconnections has been established: ' + address[0])
        except:
            all_connections.remove(conn)
            conn.close()
            print('error accepting connections')
print("IP: ",get_ip())
if __name__=='__main__':
    seer = threading.Thread(target = create_continue_server)
    seer.start()

    steam = threading.Thread(target = start_streaming)
    steam.start()













