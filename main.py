import numpy as np
import random
import math
import matplotlib.pyplot as plt
import ap
import device
from parameter import *
import optimization

t = 0
#distance between two device(AP or STA)
def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)

while t!=operation_time:
    t = t+1
    while t%30 != 0:
        for i in range(device_num):
            device.move()
            device.state_change()
        for i in range(ap_num):
            if ap.check_state_change():
                ap.action()
        t = t+1
    ap.update()

# for _ in range(10) 
ap_list = [ap(0, 0, 0, 0, 8, i, 1, 0, 1) for i in range(10)]
device_list = [device(0, 0, 1, 1, 0, 0, i, 0, 0, 1) for i in range(10)]
#再ap[0]裡面加一個device[0]
ap_list[0].adduser(device_list[0])
