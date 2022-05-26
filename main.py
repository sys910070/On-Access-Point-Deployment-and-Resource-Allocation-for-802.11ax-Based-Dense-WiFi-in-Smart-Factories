import numpy as np
import random
import math
from ap import AP 
from device import DEVICE
import device
import initialization
import optimization
import create_graph
import utils
from parameter import*

random.seed(1126)

t = 0

ap_list = [AP(random.uniform(0, 200), random.uniform(0, 180), 10, i, 1) for i in range(ap_num)]
device_list = [DEVICE(random.uniform(0, 200), random.uniform(0, 180), 2, 2, i, 1) for i in range(device_num)]

for ap_ in ap_list:
    ap_.power_change(30)   
    ap_.add_neighbor_ap(ap_list)
    
for i in range(ap_num):
    ap_list[i].channel = random.randint(1, 3)

for _ap in ap_list:
    _ap.neighbors_cci_calculation()
    
for i in range(ap_num):
    print(i, end = ' ')
    print('x ', ap_list[i].x, end = ' ')
    print('y ', ap_list[i].y)   
    print('channel ', ap_list[i].channel)
    print('neighbor ', ap_list[i].neighbor)
    print('cci ', ap_list[i].cci)

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


