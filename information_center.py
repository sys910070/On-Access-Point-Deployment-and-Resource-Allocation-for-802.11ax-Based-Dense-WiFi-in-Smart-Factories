# this file is for 0th round initailization
# ap-device association
# allocate power and frequency channel
import random
from logging.handlers import QueueListener
from ap import A_State
from device import D_State
from utils import*
from parameter import*

# AP-device association
def init(ap_list, device_list):
    initial_clear(ap_list, device_list)
    for device in device_list:
        dis = float('inf') # make dis the largest at first and update later
        selected_ap = None
        for ap in ap_list:
            if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(p_max): # in AP's max decode range
                if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                    dis = distance((device.x, device.y), (ap.x, ap.y))
                    selected_ap = ap
        if selected_ap != None:            
            device.ap = selected_ap
            selected_ap.adduser(device)
    
    # for AP with users lower than lowerbound, remove all device and connect to other AP if possible
    used_ap = {}
    while not ap_lowerbound_check(ap_list):
        for device in device_list:
            dis = float('inf')
            selected_ap = None
            if device.ap != None:
                if len(device.ap.user) < device.ap.lowerbound and len(device.ap.user) != 0:
                    device.ap.user.remove(device)
                    for ap in ap_list:
                        if device not in used_ap:
                            used_ap[device] = []
                        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(p_max) and ap != device.ap and ap not in used_ap[device]:
                            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                                dis = distance((device.x, device.y), (ap.x, ap.y))
                                selected_ap = ap
                    if selected_ap != None:            
                        device.ap = selected_ap
                        used_ap[device].append(selected_ap)
                        selected_ap.adduser(device)
                    else:
                        device.ap = None

    # for device not connected to ap, connect them to the closest ap and ap state set underpopulated
    for device in device_list:
        if device.ap == None:
            dis = float('inf')
            selected_ap = None
            for ap in ap_list:
                if ap.power == 0 and distance((device.x, device.y), (ap.x, ap.y)) < range_decode(p_max): # all AP that cover the device
                    if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                        dis = distance((device.x, device.y), (ap.x, ap.y))
                        selected_ap = ap
            if selected_ap != None:
                device.ap = selected_ap
                selected_ap.adduser(device)

    for ap in ap_list:
        if len(ap.user) != 0 and len(ap.user) >= ap.lowerbound:
            ap.state = A_State.active
            ap.timer = float('inf')
        elif len(ap.user) < ap.lowerbound and len(ap.user) > 0:
            ap.state = A_State.underpopulated
            ap.timer = a_state_timer_underpopulate
        else:
            ap.state = A_State.idle
            ap.timer = a_state_timer_idle       

    power_allocation(ap_list)            
    channel_allocation(ap_list)
    device_resource(device_list)

# allocate lowest power level to cover all associated device
def power_allocation(ap_list):
    for ap in ap_list:
        if len(ap.user) != 0:
            for power in power_level:
                if range_decode(power) >= max_dis_device(ap):
                    ap.power_change(power, ap_list)
                    break

# allocate 20MHz frequency channel
def channel_allocation(ap_list):
    # firstly sort the quene indecending order for the most users ap in the first position
    q = sorted(ap_list, key = lambda ap: len(ap.user), reverse = True)
    set_20 = set(frequency_channel_20)
    set_neighbor = set()
    for ap in q:
        if len(ap.user) == 0:
            break
        else:
            set_neighbor = {neighbor.channel for neighbor in ap.neighbor}
            set_diff = set_20.difference(set_neighbor)
            if len(set_diff) != 0:
                ap.channel = random.choice(list(set_diff))
            else:
                ap.channel = min_user_channel(ap)
    for ap in ap_list:
        ap.cci_calculation()
    # enhance all small bandwidth to large bandwith
    channel_enhancement(ap_list)

# allocate 40, 80, 160MHz frequency channel
def channel_enhancement(ap_list):
    q = sorted(ap_list, key = lambda ap: len(ap.user), reverse = True)
    channel_enhance(q, frequency_channel_40)
    channel_enhance(q, frequency_channel_80)
    channel_enhance(q, frequency_channel_160)

def device_resource(device_list):
    for device in device_list:
        if device.ap != None:
            device.channel = device.ap.channel
            device.power = device.ap.power
            device.state = D_State.connected
            device.dis_cal()
        else:
            device.state = D_State.detached
            device.timer = d_state_timer_detached