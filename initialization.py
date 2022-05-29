# this file is for 0th round initailization
# ap-device association
# allocate power and frequency channel
# nighboring ap, cci
from ap import AP 
from utils import distance

def init(ap_list, device_list):
    for device in device_list:
        dis = float('inf') # make dis the largest at first and update later
        for aps in ap_list:
            for ap in aps:
                if(distance((device.x, device.y), (ap.x, ap.y))<dis):
                    dis = distance((device.x, device.y), (ap.x, ap.y))
                    selected_ap = ap
        device.ap = selected_ap.id
        selected_ap.adduser(device.id)
