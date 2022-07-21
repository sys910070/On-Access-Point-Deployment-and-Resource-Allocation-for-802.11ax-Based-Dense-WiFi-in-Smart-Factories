#this file is for small function
from parameter import*
import random

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

def qos_requirment_throughput(device_list):
    throughput_count = 0
    for device in device_list:
        if device.throughput < device_throughput_qos:
            throughput_count += 1
    if throughput_count/device_num > device_throughput_ratio_reqirment:
        return False
    else:
        return True

# performance matric
# number of active_ap
def active_ap_count(ap_list):
    active_ap_count = 0
    for ap in ap_list:
        if ap.power!=0:
            active_ap_count += 1
    return active_ap_count

# channel conflict indicator
def cci_cal(ap_list):
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
    total_throughput_ap = 0
    total_throughput_device = 0
    for ap in ap_list:
        ap.throughput_cal()
        total_throughput_ap += ap.throughput
    for device in device_list:
        device.throughput_cal()
        total_throughput_device += device.throughput
    return total_throughput_device
    
# fairness index
def fairness_cal(ap_list):
    x1 = 0
    x2 = 0
    active_num = 0
    for ap in ap_list:
        if ap.power != 0:
            active_num += 1
            user_throughput = 0
            if len(ap.user) != 0:
                user_throughput = ap.user[0].throughput
            x1 = x1+user_throughput
            x2 = x2+user_throughput**2
    return x1**2/(active_num*x2)

def calculate_interval_average(fairness_record_interval, total_throughput_record__interval, lost_device_record_interval, active_ap_record_interval):
    fairness = sum(fairness_record_interval)/len(fairness_record_interval)
    throughput = sum(total_throughput_record__interval)/len(total_throughput_record__interval)
    lost_device = sum(lost_device_record_interval)/len(lost_device_record_interval)
    active_ap = sum(active_ap_record_interval)/len(active_ap_record_interval)
    return fairness, throughput, lost_device, active_ap

#mobility model
def mobility_real_factory(device):
    # rgv, oht
    if ((device.x == 11 or device.x == 101 or device.x == 79 or device.x == 169) and (device.y >= 16 and device.y <= 29)) or ((device.y == 16 or device.y == 29) and (device.x >= 11 and device.x <= 79) or (device.x >= 101 and device.x <= 169))\
        or ((device.x == 11 or device.x == 79) and (device.y >= 106 and device.y <= 119)) or ((device.y == 106 or device.y == 119) and (device.x >= 11 and device.x <= 79))\
        or ((device.x == 101 or device.x == 169) and (device.y >= 136 and device.y <= 149)) or ((device.y == 136 or device.y == 149) and (device.x >= 101 and device.x <= 169)):
        if (device.x == 11 or device.x == 101) and (device.y > 16 and device.y <= 29)\
            or (device.x == 11) and (device.y > 106 and device.y <= 119)\
            or (device.x == 101) and (device.y > 136 and device.y <= 149):
            device.y -= 1
        elif (device.x == 79 or device.x == 169) and (device.y >= 16 and device.y < 29)\
            or (device.x == 79) and (device.y >= 106 and device.y < 119)\
            or (device.x == 169) and (device.y >= 136 and device.y < 149):
            device.y += 1
        elif (device.y == 16 and ((device.x >= 11 and device.x < 79) or (device.x >= 101 and device.x < 169)))\
            or (device.y == 106 and ((device.x >= 11 and device.x < 79)))\
            or (device.y == 136 and ((device.x >= 101 and device.x < 169))):
            device.x += 1
        elif (device.y == 29 and ((device.x > 11 and device.x <= 79) or (device.x > 101 and device.x <= 169)))\
            or (device.y == 119 and ((device.x > 11 and device.x <= 79)))\
            or (device.y == 149 and ((device.x > 101 and device.x <= 169))):
            device.x -= 1
    # agv
    if device.x >= 10 and device.x <= 80 and device.y >= 45 and device.y <= 60:
        dis = random.randint(1, 5)
        for _ in range(dis):
            clean_area_mobility_model(device, 10, 80, 45, 60)
    if device.x >= 100 and device.x <= 170 and device.y >= 45 and device.y <= 60:
        dis = random.randint(1, 5)
        for _ in range(dis):
            clean_area_mobility_model(device, 100, 170, 45, 60)
    if device.x >= 100 and device.x <= 170 and device.y >= 75 and device.y <= 90:
        dis = random.randint(1, 5)
        for _ in range(dis):
            clean_area_mobility_model(device, 100, 170, 75, 90)
    
    # pgv
    if device.x >= 10 and device.x <= 80 and device.y >= 135 and device.y <= 150:
        dis = random.randint(1, 5)
        for _ in range(dis):
            clean_area_mobility_model(device, 10, 80, 135, 150)

def mobility(device):
    # region 5
    if device.x != 0 and device.x != 180 and device.y != 0 and device.y != 200:
        if factory_environment == 'no_obstacle':
            num = random.randint(1, 4)
            if num == 1:
                device.x += 1
            elif num == 2:
                device.x -= 1
            elif num == 3:
                device.y += 1
            else:
                device.y -= 1
        elif factory_environment == 'symmetric_obstacle':
            #sym_region 1
            if (device.x == 45 and ((device.y > 10 and device.y < 40) or (device.y > 160 and device.y < 190))) or (device.x == 10 or device.x == 140) and ((device.y > 55 and device.y < 145)):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.x -= 1
                elif num == 3:
                    device.y += 1
                else:
                    device.y -= 1
            #sym_region 2
            elif (device.y == 145 and ((device.x > 10 and device.x < 40) or (device.x > 140 and device.x < 170))) or (device.y == 40 or device.y == 190) and ((device.x > 45 and device.x < 135)):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.y += 1
                elif num == 3:
                    device.x += 1
                else:
                    device.x -= 1
            #sym_region 3
            elif (device.x == 135 and ((device.y > 10 and device.y < 40) or (device.y > 160 and device.y < 190))) or (device.x == 40 or device.x == 170) and ((device.y > 55 and device.y < 145)):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.x += 1
                elif num == 3:
                    device.y += 1
                else:
                    device.y -= 1
            #sym_region 4
            elif (device.y == 55 and ((device.x > 10 and device.x < 40) or (device.x > 140 and device.x < 170))) or (device.y == 10 or device.y == 160) and ((device.x > 45 and device.x < 135)):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.y -= 1
                elif num == 3:
                    device.x += 1
                else:
                    device.x -= 1
            else:
                num = random.randint(1, 4)
                if num == 1:
                    device.x += 1
                elif num == 2:
                    device.x -= 1
                elif num == 3:
                    device.y += 1
                else:
                    device.y -= 1

        elif factory_environment == 'asymmetric_obstacle':
            #asym_region 1
            if (device.x == 75 and (device.y > 130 and device.y < 180)) or ((device.x == 10 or device.x == 95) and ((device.y > 0 and device.y < 75))):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.x -= 1
                elif num == 3:
                    device.y += 1
                else:
                    device.y -= 1
            #asym_region 2
            elif (device.y == 75 and ((device.x > 10 and device.x < 85) or (device.x > 95 and device.x < 170))) or (device.y == 170 and (device.x > 0 and device.x < 30)) or (device.y == 180 and (device.x > 75 and device.x < 135)):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.y += 1
                elif num == 3:
                    device.x += 1
                else:
                    device.x -= 1
            #asym_region 3
            elif (device.x == 135 and (device.y > 130 and device.y < 180)) or (device.x == 30 and (device.y > 130 and device.y < 170)) or ((device.x == 85 or device.x == 170) and ((device.y > 0 and device.y < 75))):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.x += 1
                elif num == 3:
                    device.y += 1
                else:
                    device.y -= 1
            #asym_region 4
            elif (device.y == 130 and ((device.x > 0 and device.x < 30) or (device.x > 75 and device.x < 135))):
                num = random.randint(1, 4)
                if num == 1 or num == 2:
                    device.y -= 1
                elif num == 3:
                    device.x += 1
                else:
                    device.x -= 1
            else:
                num = random.randint(1, 4)
                if num == 1:
                    device.x += 1
                elif num == 2:
                    device.x -= 1
                elif num == 3:
                    device.y += 1
                else:
                    device.y -= 1

    #specific case for asymmetric obstacle()
    #asym_region 5
    elif factory_environment == 'asymmetric_obstacle' and device.y == 0 and (device.x == 10 or device.x == 95):
        num = random.randint(1, 2)
        if num == 1:
            device.x -= 1
        else:
            device.y += 1
    #asym_region 6
    elif factory_environment == 'asymmetric_obstacle' and (device.y == 0 and (device.x == 85 or device.x == 170)) or (device.x == 0 and device.y == 170):
        num = random.randint(1, 2)
        if num == 1:
            device.x += 1
        else:
            device.y += 1
    #asym_region 7
    elif factory_environment == 'asymmetric_obstacle' and device.x == 0 and device.y == 130:
        num = random.randint(1, 2)
        if num == 1:
            device.x += 1
        else:
            device.y -= 1
    # region 1
    elif device.x == 0 and device.y == 0:
        num = random.randint(1, 2)
        if num == 1:
            device.x += 1
        else:
            device.y += 1
    # region 2
    elif device.x == 0 and device.y != 0 and device.y != 200:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.x += 1
        elif num == 3:
            device.y += 1
        else:
            device.y -= 1
    # region 3
    elif device.x == 0 and device.y == 200:
        num = random.randint(1, 2)
        if num == 1:
            device.x += 1
        else:
            device.y -= 1
    # region 4
    elif device.y == 0 and device.x != 0 and device.x != 180:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.y += 1
        elif num == 3:
            device.x += 1
        else:
            device.x -= 1
    # region 6
    elif device.y == 200 and device.x != 0 and device.x != 180:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.y -= 1
        elif num == 3:
            device.x += 1
        else:
            device.x -= 1
    # region 7
    elif device.x == 180 and device.y == 0:
        num = random.randint(1, 2)
        if num == 1:
            device.x -= 1
        else:
            device.y += 1
    # region 8
    elif device.x == 180 and device.y != 0 and device.y != 200:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.x -= 1
        elif num == 3:
            device.y += 1
        else:
            device.y -= 1
    # region 9
    elif device.x == 180 and device.y == 200:
        num = random.randint(1, 2)
        if num == 1:
            device.x -= 1
        else:
            device.y -= 1

def clean_area_mobility_model(device, x_min, x_max, y_min, y_max):
    #region 5
    if device.x != x_min and device.x != x_max and device.y != y_min and device.y != y_max:
        num = random.randint(1, 4)
        if num == 1:
            device.x += 1
        elif num == 2:
            device.x -= 1
        elif num == 3:
            device.y += 1
        else:
            device.y -= 1
    # region 1
    elif device.x == x_min and device.y == y_min:
        num = random.randint(1, 2)
        if num == 1:
            device.x += 1
        else:
            device.y += 1
    # region 2
    elif device.x == x_min and device.y != y_min and device.y != y_max:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.x += 1
        elif num == 3:
            device.y += 1
        else:
            device.y -= 1
    # region 3
    elif device.x == x_min and device.y == y_max:
        num = random.randint(1, 2)
        if num == 1:
            device.x += 1
        else:
            device.y -= 1
    # region 4
    elif device.y == y_min and device.x != x_min and device.x != x_max:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.y += 1
        elif num == 3:
            device.x += 1
        else:
            device.x -= 1
    # region 6
    elif device.y == y_max and device.x != x_min and device.x != x_max:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.y -= 1
        elif num == 3:
            device.x += 1
        else:
            device.x -= 1
    # region 7
    elif device.x == x_max and device.y == y_min:
        num = random.randint(1, 2)
        if num == 1:
            device.x -= 1
        else:
            device.y += 1
    # region 8
    elif device.x == x_max and device.y != y_min and device.y != y_max:
        num = random.randint(1, 4)
        if num == 1 or num == 2:
            device.x -= 1
        elif num == 3:
            device.y += 1
        else:
            device.y -= 1
    # region 9
    elif device.x == x_max and device.y == y_max:
        num = random.randint(1, 2)
        if num == 1:
            device.x -= 1
        else:
            device.y -= 1