import random
from itertools import chain
from parameter import*
from ap import AP
from device import DEVICE

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
        if symmetric_obstacle(x, y):
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
        if asymmetric_obstacle(x, y):
            device_list.append(DEVICE(x, y, device_count+1, Type.throughput))
            device_count += 1
    # make half of device type 2
    for i in range(len(device_list)):
        if i%2 != 0:
            device_list[i].type = Type.delay
    return device_list

def create_device_real_factory_layout():
    dic = {} 
    rgv_list = []
    agv_list = []
    pgv_list = []
    oht_list = []
    device_list = []
    type1_list = []
    device_count = 0

    # create rgv device
    rgv_count = 0
    rgv_pos = []
    for i in range(11, 80):
        rgv_pos.append((i, 16))
        rgv_pos.append((i, 29))
    for i in range(17, 29):
        rgv_pos.append((11, i))
        rgv_pos.append((79, i))
    for i in range(101, 170):
        rgv_pos.append((i, 16))
        rgv_pos.append((i, 29))
    for i in range(17, 29):
        rgv_pos.append((101, i))
        rgv_pos.append((170, i))
    while rgv_count != rgv_num:
        flag = True
        while flag:
            pos = random.choice(list(rgv_pos))
            if pos not in dic:
                dic[pos] = dic.setdefault(pos, 0)
                rgv_list.append(DEVICE(pos[0], pos[1], device_count+1, Type.delay))
                device_count += 1
                rgv_count += 1
                flag = False

    # create oht device
    oht_count = 0
    oht_pos = []
    for i in range(11, 80):
        oht_pos.append((i, 106))
        oht_pos.append((i, 119))
    for i in range(107, 119):
        oht_pos.append((11, i))
        oht_pos.append((79, i))

    for i in range(101, 170):
        oht_pos.append((i, 136))
        oht_pos.append((i, 149))
    for i in range(137, 149):
        oht_pos.append((101, i))
        oht_pos.append((170, i))
    while oht_count != oht_num:
        flag = True
        while flag:
            pos = random.choice(list(oht_pos))
            if pos not in dic:
                dic[pos] = dic.setdefault(pos, 0)
                oht_list.append(DEVICE(pos[0], pos[1], device_count+1, Type.delay))
                device_count += 1
                oht_count += 1
                flag = False
        
    # create agv device
    agv_count = 0
    agv_pos = []
    for i in range(10, 81):
        for j in range(45, 61):
            agv_pos.append((i, j))
    for i in range(100, 171):
        for j in range(45, 61):
            agv_pos.append((i, j))
    for i in range(100, 171):
        for j in range(75, 91):
            agv_pos.append((i, j))
    
    while agv_count != agv_num:
        flag = True
        while flag:
            pos = random.choice(list(agv_pos))
            if pos not in dic:
                dic[pos] = dic.setdefault(pos, 0)
                agv_list.append(DEVICE(pos[0], pos[1], device_count+1, Type.delay))
                device_count += 1
                agv_count += 1
                flag = False

    # create pgv device
    pgv_count = 0
    pgv_pos = []
    for i in range(10, 81):
        for j in range(135, 151):
            pgv_pos.append((i, j))
    
    while pgv_count != pgv_num:
        flag = True
        while flag:
            pos = random.choice(list(pgv_pos))
            if pos not in dic:
                dic[pos] = dic.setdefault(pos, 0)
                pgv_list.append(DEVICE(pos[0], pos[1], device_count+1, Type.delay))
                device_count += 1
                pgv_count += 1
                flag = False

    # create type 1 device
    for i in range(1, 6):
        type1_list.append(DEVICE(10+i*12, 75, device_count+1, Type.throughput))
        device_count += 1
        type1_list.append(DEVICE(10+i*12, 90, device_count+1, Type.throughput))
        device_count += 1
        type1_list.append(DEVICE(100+i*12, 105, device_count+1, Type.throughput))
        device_count += 1
        type1_list.append(DEVICE(100+i*12, 120, device_count+1, Type.throughput))
        device_count += 1

    for device in rgv_list:
        device.gv = 1
        device_list.append(device)
    for device in oht_list:
        device.gv = 2
        device_list.append(device)
    for device in agv_list:
        device.gv = 3
        device_list.append(device)
    for device in pgv_list:
        device.gv = 4
        device_list.append(device)
    for device in type1_list:
        device_list.append(device)
    
    return device_list