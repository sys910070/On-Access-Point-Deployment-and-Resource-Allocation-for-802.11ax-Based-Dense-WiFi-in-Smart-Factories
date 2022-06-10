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
    # choose next AP to connect but not the previous one
    selected_ap = find_ap(device, ap_list)
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
    device.state = D_State.detached
# d
def detached_detached(device, _):
    device.timer = d_state_timer_detached
# e
def detached_connected(device, ap_list):
    selected_ap = find_ap(device, ap_list)
    if selected_ap != None:  
        device.ap = selected_ap
        device.power = device.ap.power
        device.channel = device.ap.channel
        device.state = D_State.connected
        device.timer = float('inf')
        selected_ap.adduser(device)
# f
def connected_handover(device, _):
    device.timer = d_state_timer_handover
    device.state = D_State.handover
# g
def handover_connected(device, ap_list):
    selected_ap = find_ap(device, ap_list)
    if selected_ap != None: 
        if selected_ap != device.ap:
            device.ap.user.remove(device)
            device.ap = selected_ap
            device.power = device.ap.power
            device.channel = device.ap.channel
            device.state = D_State.connected
            device.timer = float('inf')
            selected_ap.adduser(device)
        else:
            device.timer = float('inf')
            device.state = D_State.connected
# h
def handover_detached(device, _):
    device.power = 0
    device.channel = 0
    device.ap.user.remove(device)
    device.ap = None
    device.timer = d_state_timer_detached
    device.state = D_State.detached
