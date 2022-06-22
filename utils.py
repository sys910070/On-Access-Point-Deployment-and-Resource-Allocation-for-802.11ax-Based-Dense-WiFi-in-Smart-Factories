#this file is for small function
import matplotlib.pyplot as plt
from parameter import*
import random
import logging
import pygame

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
    
def all_timer_minus_one(device_list, ap_list):
    for device in device_list:
        device.timer -= 1
    for ap in ap_list:
        ap.timer -= 1    

# device find the active ap based on the closest distance 
def find_active_ap(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power): # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    return selected_ap

# device find ap but not the one it is connecting right now    
def find_other_active_ap(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power) and ap != device.ap: # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) < ap.upperbound:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    return selected_ap

# for an ap, check if there are devices select it as service ap
def selected_device_check(ap, device_list):
    for device in device_list:
        if device.selected == ap:
            return True
    return False

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

# initialization: allocate 20, 40, 80, 160 channel to initial
def channel_enhance(q, channel_list):
    for ap in q:
        pre_cci = ap.cci
        if len(ap.user) == 0:
            break
        else:
            for channel in channel_list:
                for ch in ch_dic[channel]:
                    if ap.channel == ch:
                        temp_channel = ap.channel
                        ap.channel = channel
                        ap.cci_calculation()
                        if ap.cci != pre_cci:
                            ap.cci = pre_cci
                            ap.channel = temp_channel
                        break

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

def log_info(ap_list, device_list):
    # open a log file
    ap_logger = setup_logger('AP', 'AP.txt')                    # open file
    device_logger = setup_logger('Device', 'Device.txt')        # open file
    ap_logger.info('id, users, power, state, timer')
    for ap in ap_list:    
        ap_logger.info(f'{ap.id}, {ap.power}, {ap.throughput}')
    device_logger.info('id, ap, power, state, timer, x, y')
    for device in device_list:
        if device.ap != None:
            device_logger.info(f'{device.id}, {device.ap.id}, {device.power}, {device.state.name}, {device.timer}, {device.throughput}')
        else:
            device_logger.info(f'{device.id}, {None}, {device.power}, {device.state.name}, {device.timer}, {device.throughput}')
    
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

# check the whole system if there is a device connected to two different ap
def check_device_connect_one_ap(ap_list):
    for ap in ap_list:
        for user in ap.user:
            for other_ap in ap_list: 
                for other_ap_user in other_ap.user:
                    if other_ap != ap and user == other_ap_user:
                        return user  

# check feasibility
# disconnected device count
def loss_device_count(device_list):
    count = 0
    for device in device_list:
        if device.ap == None:
            count += 1
    return count

def everything_ok(ap_list, device_list):
    for ap in ap_list:
        if not ap.ok():
            return False
    for device in device_list:
        if not device.ok():
            return False
    return True

# performance matric
# channel conflict indicator
def cci_calculation(ap_list):
    for ap in ap_list:
        if ap.power != 0:
            ap.cci = 0
            for neighbor in ap.neighbor:
                for ch in ch_dic[neighbor.channel]:
                    if ch == ap.channel:
                        ap.cci = ap.cci + 1
        else:
            ap.cci = 0

# throughput calculation
def throughput_cal(ap_list, device_list):
    for ap in ap_list:
        ap.throughput_cal()
    for device in device_list:
        device.throughput_cal()

# fairness index
def fairness(ap_list):
    x1 = 0
    x2 = 0
    for ap in ap_list:
        if len(ap.user) != 0:
            user_throughput = ap.user[0].throughput
        x1 = x1+user_throughput
        x2 = x2+user_throughput**2
    return x1**2/(ap_num*x2)

# animation text
def txt(obj):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render(str(obj.id), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (obj.y+10, obj.x-10)
    return text, textRect