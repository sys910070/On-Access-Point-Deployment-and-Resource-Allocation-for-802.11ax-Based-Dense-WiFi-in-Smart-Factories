#this file is for small function
import matplotlib.pyplot as plt
from parameter import*
import random
import logging

#distance between two device(AP or STA)
def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)

# communication range or decode range
def range_decode(power):
    if power != 0:
        return 10**((power+GTX+GRX-P_REF-CHI-THETA_DECODE)/(10*ETA))
    else:
        return 0

# communication range or interference range
def range_interference(power):
    if power != 0:
        return 10**((power+GTX+GRX-P_REF-CHI-THETA_INTERFERENCE)/(10*ETA))
    else:
        return 0

# return True if all ap's users number > each ap's lowerbound
def ap_lowerbound_check(ap_list):
    for ap in ap_list:
        if len(ap.user) < ap.lowerbound and len(ap.user) != 0:
            return False
    return True

# the maximum distance device in an ap
def max_dis_device(ap):
    dis = 0
    for device in ap.user:
        if distance((device.x, device.y), (ap.x, ap.y)) > dis:
            dis = distance((device.x, device.y), (ap.x, ap.y))
    return dis

# check if channels are overlapped
def overlap(ch1, ch2):
    for channel in ch_dic[ch1]:
        if channel == ch2:
            return True
    return False

# find the channel with minimum neighbor using
def min_user_channel(ap):
    def find_min_user_channel(dic):
        min_user = float("inf")
        candidate_channel = []
        for key, value in dic.items():
            if value < min_user:
                min_user = value
                candidate_channel = [key]
            elif value == min_user:
                candidate_channel.append(key)
        return random.choice(candidate_channel)
    dic = {}
    for neighbor in ap.neighbor:
        if neighbor.channel == 0:
            continue
        if neighbor.channel not in dic.keys():
            dic[neighbor.channel] = 1
        else:
            dic[neighbor.channel] += 1
    return find_min_user_channel(dic)
    
def initial_clear(ap_list, device_list):
    for ap in ap_list:
        ap.power = 0
        ap.channel = 0
        ap.user = []
        ap.neighbor = []

    for device in device_list:
        device.ap = None
        device.power = 0
        device.channel = 0

# device find the ap based on the strongest signal 
def find_ap(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power): # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    return selected_ap

# device find ap but not the one it is connecting right now    
def find_other_ap(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power) and ap != device.ap: # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    return selected_ap

def device_connect(device, ap):
    ap.adduser(device)
    device.ap = ap
    device.power = ap.power
    device.channel = ap.channel

def device_disconnect(device):
    device.ap.user.remove(device)
    device.ap = None
    device.power = 0
    device.channel = 0

# only 20 MHz channel would be selected (revise lated)
def select_channel(ap, ap_list):
    set_20 = set(frequency_channel_20)
    set_neighbor = set()
    set_neighbor = {neighbor.channel for neighbor in ap.neighbor}
    set_diff = set_20.difference(set_neighbor)
    if len(set_diff) != 0:
        ap.channel = random.choice(list(set_diff))
    else:
        ap.channel = min_user_channel(ap)

def power_adjustment(ap, ap_list):
    if len(ap.user) != 0:
        for power in power_level:
            if range_decode(power) >= max_dis_device(ap):
                ap.power_change(power, ap_list)
                break

# log file
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

#graph
def graph_device(ap_list, device_list):
    plt.title('simulation display')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
   
    for ap in ap_list:
        if ap.channel == 0:
            continue
        elif ch_id_to_bw[ap.channel] == 20:
            plt.plot(ap.y, ap.x,'ro', color = 'lime') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='lime')
        elif ch_id_to_bw[ap.channel] == 40:
            plt.plot(ap.y, ap.x,'ro', color = 'red') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='red')
        elif ch_id_to_bw[ap.channel] == 80:
            plt.plot(ap.y, ap.x,'ro', color = 'blue') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='blue')
        elif ch_id_to_bw[ap.channel] == 160:
            plt.plot(ap.y, ap.x,'ro', color = 'purple') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='purple')
    for device in device_list:
        if device.ap != None:
            plt.plot(device.y, device.x, 'ro', color = 'black') # device
            plt.text(device.y+1, device.x+1, device.id, color='black')
        else:
            plt.plot(device.y, device.x, 'ro', color = 'dimgrey') # device
            plt.text(device.y+1, device.x+1, device.id, color='dimgrey')
    plt.axis([0, factory_width, 0, factory_length])
    plt.show()

# performance matric
# disconnected device count
def loss_device_count(device_list):
    count = 0
    for device in device_list:
        if device.ap == None:
            count += 1
    return count

# fairness index
def fairness(ap_list):
    x1 = 0
    x2 = 0
    for ap in ap_list:
        x1 = x1+ap.throughput/len(ap.user)
        x2 = x2+(ap.throughput/len(ap.user))**2
    return x1**2/(ap_num*x2)