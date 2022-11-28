#!/usr/bin/env python3

import sys
import os
import rospy

from Classes.Detection_input import Listener_det
From swarm.msg import Detection

def main():
    #Initialize ROS node
    rospy.init_node('detection_node', anonymous=True)
    rospy.logdebug("Started detection node")
    
    #initiate listener socket
    pub = Listener_det()
    
    #Starting listening and handling data from detection_input
    rospy.loginfo("Starting run")
    pub.run_det()
    rospy.loginfo("Shutting down")

    if __name__ = '__main__':
        main()
