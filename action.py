# device's action and AP's action
from enum import(IntEnum, unique)
from utils import*

@unique
class D_State(IntEnum):
    init = 1
    connected = 2
    detached = 3
    handover = 4

# device action(action a and action h are both set initially)
# b(device connect from one AP to another AP)
def connected_connected(device, ap_list):
    dis = float('inf')
    selected_ap = None
    # choose next AP to connect but not the previous one
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power): # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound and ap != device.ap:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    if device.ap != None:
        device.ap.user.remove(device)         
        device.ap = selected_ap
        device.channel = device.ap.channel
        device.power = device.ap.power
        selected_ap.adduser(device)
# c
def connected_detached(device, _):
    device.power = 0
    device.channel = 0
    device.ap.user.remove(device)
    device.ap = None
    device.timer = d_state_timer_detached
    device.type = D_State.detached
# d
def detached_detached(device, _):
    device.timer = d_state_timer_detached
# e
def detached_connected(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power): # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    if selected_ap != None:  
        device.ap = selected_ap
        device.power = device.ap.power
        device.channel = device.ap.channel
        device.type = D_State.connected
        device.timer = float('inf')
        selected_ap.adduser(device)
# f
def connected_handover(device, _):
    device.timer = d_state_timer_handover
    device.type = D_State.handover
# g
def handover_connected(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power): # all AP that cover the device
            if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                dis = distance((device.x, device.y), (ap.x, ap.y))
                selected_ap = ap
    if selected_ap != None:  
        device.ap = selected_ap
        device.power = device.ap.power
        device.channel = device.ap.channel
        device.type = D_State.connected
        device.timer = float('inf')
        selected_ap.adduser(device)
# h
def handover_detached(device, _):
    device.power = 0
    device.channel = 0
    device.ap.user.remove(device)
    device.ap = None
    device.timer = d_state_timer_detached
    device.type = D_State.detached
