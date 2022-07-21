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

# allocate lowest power level to cover all associated device
def power_allocation(ap_list):
    for ap in ap_list:
        if len(ap.user) != 0:
            ap.power_change(p_max, ap_list)

# randomly allocate all frequency channel
def channel_allocation(ap_list):
    # firstly sort the quene indecending order for the most users ap in the first position
    q = sorted(ap_list, key = lambda ap: len(ap.user), reverse = True)
    channel_list = []
    for i in range(1, 20):
        channel_list.append(i)
    channel_list.reverse()
    for ap in q:
        temp_channel = 0
        temp_cci = float('inf')
        for channel in channel_list:
            ap.channel = channel
            temp_cci_cal(ap_list)
            if ap.cci < temp_cci:
                temp_cci = ap.cci
                temp_channel = channel
        ap.channel = temp_channel
        for user in ap.user:
            user.channel = ap.channel
