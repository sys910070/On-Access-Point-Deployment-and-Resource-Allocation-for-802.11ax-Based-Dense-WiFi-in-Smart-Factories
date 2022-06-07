# this file is for 0th round initailization
# ap-device association
# allocate power and frequency channel
# nighboring ap, cci
import random
from logging.handlers import QueueListener
from ap import AP 
from utils import*
from parameter import*

# initialization
def init(ap_list, device_list):
    for device in device_list:
        dis = float('inf') # make dis the largest at first and update later
        selected_ap = None
        for ap in ap_list:
            if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(30): # in AP's max decode range
                if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                    dis = distance((device.x, device.y), (ap.x, ap.y))
                    selected_ap = ap
        if selected_ap != None:            
            device.ap = selected_ap
            selected_ap.adduser(device)
    
    # if an AP with users lower than lowerbound remove all device and connect to other AP
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
                        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(30) and ap != device.ap and ap not in used_ap[device]:
                            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                                dis = distance((device.x, device.y), (ap.x, ap.y))
                                selected_ap = ap
                    if selected_ap != None:            
                        device.ap = selected_ap
                        used_ap[device].append(selected_ap)
                        selected_ap.adduser(device)
                    else:
                        device.ap = None                        

# allocate lowest power level to cover all associated device
def power_allocation(ap_list):
    for ap in ap_list:
        if len(ap.user) != 0:
            for power in power_level:
                if range_decode(power) >= max_dis_device(ap):
                    ap.power_change(power)
                    break
    for ap in ap_list:
        ap.add_neighbor_ap(ap_list)

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
                # ap.channel = random.choice(list(set_20))
                ap.channel = min_user_channel(ap)
    for ap in ap_list:
        ap.cci_calculation()

# allocate 40, 80, 160MHz frequency channel
def channel_enhancement(ap_list):
    q = sorted(ap_list, key = lambda ap: len(ap.user), reverse = True)
    # 40MGz channel allocation
    for ap in q:
        pre_cci = ap.cci
        if len(ap.user) == 0:
            break
        else:
            for ch_40 in frequency_channel_40:
                for ch in ch_dic[ch_40]:
                    if ap.channel == ch:
                        temp_channel = ap.channel
                        ap.channel = ch_40
                        ap.cci_calculation()
                        if ap.cci != pre_cci:
                            ap.cci = pre_cci
                            ap.channel = temp_channel
                        break
    # 80MGz channel allocation                
    for ap in q:
        pre_cci = ap.cci
        if len(ap.user) == 0:
            break
        else:
            for ch_80 in frequency_channel_80:
                for ch in ch_dic[ch_80]:
                    if ap.channel == ch:
                        temp_channel = ap.channel
                        ap.channel = ch_80
                        ap.cci_calculation()
                        if ap.cci != pre_cci:
                            ap.cci = pre_cci
                            ap.channel = temp_channel
                        break
    # 160MGz channel allocation
    for ap in q:
        pre_cci = ap.cci
        if len(ap.user) == 0:
            break
        else:
            for ch_160 in frequency_channel_160:
                for ch in ch_dic[ch_160]:
                    if ap.channel == ch:
                        temp_channel = ap.channel
                        ap.channel = ch_160
                        ap.cci_calculation()
                        if ap.cci != pre_cci:
                            ap.cci = pre_cci
                            ap.channel = temp_channel
                        break
