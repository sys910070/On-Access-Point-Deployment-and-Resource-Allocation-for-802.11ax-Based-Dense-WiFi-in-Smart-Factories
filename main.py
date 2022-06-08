import numpy as np
import random
import math
from itertools import chain
from ap import AP 
from device import DEVICE
from information_center import*
import optimization
from utils import* 
from parameter import*
import logging

# create two log file for APs and devices
formatter = logging.Formatter('%(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file, mode='w')        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []
    logger.addHandler(handler)

    return logger

random.seed(1126)
# set global timer to 0
t = 0

# first simulation setup
# creare ap list
temp_ap = [[AP(18 * (i + 1), 20 * (j + 1), 9 * i + j + 1, 1) for j in range(9)] for i in range(9)] #2D array
# turn 2D list into 1D list
ap_list = list(chain.from_iterable(temp_ap))
# make half of AP type 2 and assign lowerbound, uppperbound
for i in range(len(ap_list)):
    if i%2 != 0:
        ap_list[i].type = 2
        ap_list[i].lowerbound = lowerbound2
        ap_list[i].upperbound = upperbound2
    else:
        ap_list[i].lowerbound = lowerbound1
        ap_list[i].upperbound = upperbound1

# create device list
device_list = [DEVICE(random.uniform(0, 180), random.uniform(0, 200), random.randint(1, 3), random.randint(1, 3), i+1, 1) for i in range(device_num1+device_num2)]
# make half of device type 2
for i in range(len(device_list)):
    if i%2 != 0:
        device_list[i].type = 2

# initialization
init(ap_list, device_list) 
power_allocation(ap_list)
channel_allocation(ap_list)
channel_enhancement(ap_list)
device_resource(device_list)

# simulation starts
while t!=operation_time:
    # open a log file
    ap_logger = setup_logger('AP', 'AP.txt')                    # open file
    device_logger = setup_logger('Device', 'Device.txt')        # open file

    for device in device_list:
        device.move()
    for device in device_list:
        if device.state_change(ap_list):
            pass
        
    ap_logger.info('id, users, power, channel, cci, neighbor, neighbor channel')
    for ap in ap_list:    
        ap_logger.info(f'{ap.id}, {[user.id for user in ap.user]}, {ap.power}, {ap.channel}, {ap.cci}, {[neighbor.id for neighbor in ap.neighbor]}, {[neighbor.channel for neighbor in ap.neighbor]}')
    device_logger.info('id, ap')
    for device in device_list:
        if device.ap != None:
            device_logger.info(f'{device.id}, {device.ap.id}, {device.power}, {device.channel}')
        else:
            device_logger.info(f'{device.id}, {0}, {device.power}, {device.channel}')
    # graph
    graph_device(ap_list, device_list)
    for device in device_list:
        device.move()
    t = t+1

# while t!=operation_time:
#     t = t+1
#     while t%30 != 0:
#         for device in device_list:
#             device.move()
#         for device in device_list:
#             if device.state_change():
#                 device.action()
#                 device.association()
#             else:
#                 continue
#         for ap in ap_list:
#             if ap.check_state_change():
#                 ap.action()
#             else:
#                 continue
#         t = t+1
#     ap.update()