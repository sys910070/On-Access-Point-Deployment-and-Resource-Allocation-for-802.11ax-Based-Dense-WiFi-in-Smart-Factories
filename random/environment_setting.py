import random
from itertools import chain
from parameter import*
from ap import AP
from device import DEVICE
random.seed(1126)
# function if device hit boundary return False, else return True
# no obstacle    
def create_ap():
    # creare ap list
    temp_ap = [[AP(18 * (i + 1), 20 * (j + 1), 9 * i + j + 1, Type.throughput) for j in range(9)] for i in range(9)] #2D array
    # turn 2D list into 1D list
    ap_list = list(chain.from_iterable(temp_ap))
    # make half of AP type 2 and assign lowerbound, uppperbound
    for i in range(len(ap_list)):
        if i%2 != 0:
            ap_list[i].type = Type.delay
            ap_list[i].lowerbound = lowerbound_delay
            ap_list[i].upperbound = upperbound_delay
        else:
            ap_list[i].lowerbound = lowerbound_throughput
            ap_list[i].upperbound = upperbound_throughput
    return ap_list

def create_device_no_obstacle():
    # create device list
    device_list = [DEVICE(random.randint(0, 180), random.randint(0, 200), i+1, Type.throughput) for i in range(device_num1+device_num2)]
    # make half of device type 2
    for i in range(len(device_list)):
        if i%2 != 0:
            device_list[i].type = Type.delay
    return device_list

# symmetric obstacle
def create_device_symmetric_obstacle():
    device_count = 0
    device_list = []
    while device_count != device_num:
        x = random.randint(0, 180)
        y = random.randint(0, 200)
        if boundary_symmetric_obstacle(x, y):
            device_list.append(DEVICE(x, y, device_count+1, Type.throughput))
            device_count += 1

    # make half of device type 2
    for i in range(len(device_list)):
        if i%2 != 0:
            device_list[i].type = Type.delay
    return device_list

# asymmetric obstacle
def create_device_asymmetric_obstacle():
    device_count = 0
    device_list = []
    while device_count != device_num:
        x = random.randint(0, 180)
        y = random.randint(0, 200)
        if boundary_asymmetric_obstacle(x, y):
            device_list.append(DEVICE(x, y, device_count+1, Type.throughput))
            device_count += 1
    # make half of device type 2
    for i in range(len(device_list)):
        if i%2 != 0:
            device_list[i].type = Type.delay
    return device_list

## test
# x = random.randint(0, 180)
# y = random.randint(0, 200)
# print(x, y)
# print(boundary_symmetric_obstacle(x, y))