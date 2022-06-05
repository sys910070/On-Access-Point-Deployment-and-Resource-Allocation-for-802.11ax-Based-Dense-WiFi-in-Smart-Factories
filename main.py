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
    logger.addHandler(handler)

    return logger

ap_logger = setup_logger('AP', 'AP.txt')
device_logger = setup_logger('Device', 'Device.txt')

random.seed(1126)

t = 0

# first simulation setup
# creare ap list
temp_ap = [[AP(18 * (i + 1), 20 * (j + 1),10, 9 * i + j + 1, 1) for j in range(9)] for i in range(9)] #2D array
# turn 2D list into 1D list
ap_list = list(chain.from_iterable(temp_ap))

# create device list
device_list = [DEVICE(random.uniform(0, 180), random.uniform(0, 200), random.randint(1, 3), random.randint(1, 3), i+1, 1) for i in range(device_num)]

# initialization
init(ap_list, device_list) 
power_allocation(ap_list)
channel_allocation(ap_list)
channel_enhancement(ap_list)

ap_logger.info('id, users, power, channel, cci, neighbor, neighbor channel')
for ap in ap_list:    
    ap_logger.info(f'{ap.id}, {[user.id for user in ap.user]}, {ap.power}, {ap.channel}, {ap.cci}, {[neighbor.id for neighbor in ap.neighbor]}, {[neighbor.channel for neighbor in ap.neighbor]}')

device_logger.info('id, ap')
for device in device_list:
    device_logger.info(f'{device.id}, {device.ap.id}')

# while t!=operation_time:
#     t = t+1
#     for device in device_list:
#         device.move()
graph_device(ap_list, device_list)
  
# while t!=operation_time:
#     t = t+1
#     while t%30 != 0:
#         for _device in device_list:
#             _device.move()
#             if _device.state_change():
#                 _device.action()
#                 _device.association()
#             else:
#                 continue
#         for _ap in ap_list:
#             if _ap.check_state_change():
#                 _ap.action()
#             else:
#                 continue
#         t = t+1
#     _ap.update()