# IN COMPUTER
# This will be client
import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import requests,json
import time
import threading
# set post server host
PORT = 8082
HOST = '1.171.166.238'
# show the stream
def streaming():
    try:
        # create client server connect
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((HOST, PORT))
        data = b''
        # data = L + len(data) + data
        payload_size = struct.calcsize("L")
        print("connect sucess")
        while True:
            # len(data)
            while len(data) < payload_size:
                data += clientsocket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            # data
            while len(data) < msg_size:
                data += clientsocket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame=pickle.loads(frame_data)
            #show
            cv2.imshow('frame', frame)
            cv2.waitKey(10)
    except:
        print('waiting for stream start...')
        time.sleep(5)
        streaming()
if __name__=="__main__":
    
    streaming()
