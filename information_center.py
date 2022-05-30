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
        for aps in ap_list:
            for ap in aps:
                if(distance((device.x, device.y), (ap.x, ap.y))<dis):
                    dis = distance((device.x, device.y), (ap.x, ap.y))
                    selected_ap = ap
        device.ap = selected_ap.id
        selected_ap.adduser(device)

# allocate lowest power level to cover all associated device
def power_allocation(ap_list):
    for aps in ap_list:
        for ap in aps:
            if len(ap.user) != 0:
                for power in power_level:
                    if range_(power) >= max_dis_device(ap):
                        ap.power_change(power)
                        break
    for aps in ap_list:
        for ap in aps:
            ap.add_neighbor_ap(ap_list)

# allocate 20MHz frequency channel
def channel_allocation(id_to_ap):
    # firstly sort the quene indecending order for the most users ap in the first position
    q = sorted(id_to_ap.values(), key = lambda ap: len(ap.user), reverse = True)
    set_20 = set(frequency_channel_20)
    set_neighbor = set()
    for ap in q:
        if len(ap.user) == 0:
            continue
        else:
            set_neighbor = {id_to_ap[neighbor_id].channel for neighbor_id in ap.neighbor}
            set_diff = set_20.difference(set_neighbor)
            if len(set_diff) != 0:
                ap.channel = random.choice(list(set_diff))
            else:
                ap.channel = random.choice(list(set_20))

# allocate 40, 80, 160MHz frequency channel
def channel_enhancement(id_to_ap):
    pass