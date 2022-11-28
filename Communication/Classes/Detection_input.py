#!/usr/bin/env python3

import sys
import rospy
import json
import re
import socket
import time

from swarm.msg import Detection
from swarm.msg import SwarmHeader

bearing = 0.0
detection = false

class Listener_det(object):
    
    def get_ID(self):
        #Helper function to return ID to boat based on current IP
        IDs = {"192.168.136.61" : 0,
               "192.168.136.62" : 1,
               "192.168.136.63" : 2,
               "192.168.136.64" : 3,
               "192.168.136.65" : 4,}
        IP = self._get_ip()
        
        try:
            return IDs[IP]
        except KeyError:
            return 0
    
    def _get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.136.60", 80))
        return s.getsockname()[0]
    
    def __init__(self):
        topic_detection = "/boat/data/det"
        self.detectionPublisher = rospy.Publisher(topic_detection, Detection, queue_size = 50)
        self.header = SwarmHeader()
        self.detection_status = Detection()
        self.BOAT_ID = self.get_ID()
    
    def background_controller (self):
        s = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
        s.bind(("192.168.136.63", 9091))
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
                        self._publish_Detection(dataFromClient0, dataFromClient1)
                        conn.send("Packet received!".encode());
                except(ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    break
                    
        def get_header(self, msgtype = 4):
            time_now            = rospy.get_rostime()
            self.header.secs    = time_now.secs
            self.header.nsecs   = time_now.nsecs
            self.header.id      = self.BOAT_ID
            self.header.msgType = msgtype
            
        def _publish_Detection(self, bearing, detection):
            self.detection_status.header = self.get_header()
            self.detection_status.relative_bearing = bearing
            self.detection_status.right_detection = detection
            self.detectionPublisher.publish(self.detection_status)
            
        def run_det(self):
            self.background_controller()
