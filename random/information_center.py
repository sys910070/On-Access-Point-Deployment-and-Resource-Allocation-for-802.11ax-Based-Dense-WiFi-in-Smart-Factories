# this file is for 0th round initailization
# ap-device association
# allocate power and frequency channel
import random
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

    power_allocation(ap_list)            
    channel_allocation(ap_list)
    cci_cal(ap_list)  
    throughput_cal(ap_list, device_list)

# allocate the maximum power level to cover all associated device
def power_allocation(ap_list):
    for ap in ap_list:
        if len(ap.user) != 0:
            ap.power_change(p_max, ap_list)

# randomly allocate all frequency channel
def channel_allocation(ap_list):
    for ap in ap_list:
        if len(ap.user)!=0:
            ap.channel = random.randint(1, 19)