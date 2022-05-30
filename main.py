import numpy as np
import random
import math
from ap import AP 
from device import DEVICE
from information_center import*
import optimization
from utils import* 
from parameter import*

random.seed(1126)

t = 0

# first simulation setup
# creare ap list
ap_list = [[AP(18 * (i + 1), 20 * (j + 1),10, 9 * i + j + 1, 1) for j in range(9)] for i in range(9)] #2D array
# dictionay map 2d to 1d
id_to_ap = {}
for aps in ap_list:
    for ap in aps:
        id_to_ap[ap.id] = ap

# create device list
device_list = [DEVICE(random.uniform(0, 180), random.uniform(0, 200), random.randint(1, 3), random.randint(1, 3), i+1, 1) for i in range(device_num)]

# initialization
init(ap_list, device_list) 
power_allocation(ap_list)
channel_allocation(id_to_ap)

for aps in ap_list:    
    for ap in aps:
        print(ap.id, [user.id for user in ap.user], ap.power, ap.neighbor)

for devices in device_list:
    print(devices.id, devices.ap)

graph_device(ap_list, device_list)

# for _ap in ap_list:
#     _ap.neighbors_cci_calculation()

while t!=operation_time:
    t = t+1
    while t%30 != 0:
        for _device in device_list:
            _device.move()
            if _device.state_change():
                _device.action()
                _device.association()
            else:
                continue
        for _ap in ap_list:
            if _ap.check_state_change():
                _ap.action()
            else:
                continue
        t = t+1
    _ap.update()