import socket
import re
import json


def background_controller (dataFromClient0, dataFromClient1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("192.168.1.103", 9091))
        s.listen()
        conn, addr = s.accept();

        with conn:
            print("Accepted a connection request from %s:%s"%(addr[0], addr[1]));

            while (True):
                try:
                    dataFromClient = conn.recv(1024)
                    dataFromClient = dataFromClient.decode();
                    if(dataFromClient == ''):
                        conn.send("Nothing sent!".encode());
                    if(dataFromClient != ''):
                        dataFromClient = json.loads(dataFromClient)
                        dataFromClient0 = dataFromClient["bearing"]
                        dataFromClient1 = dataFromClient["Detection"]
                        #rel_bear = dataFromClient
                        #print(type(dataFromClient))
                        #print("Float value = ", dataFromClient0)
                        #print("Bool value = ", dataFromClient1)
                        conn.send("Packet received!".encode());
                except(ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    break
