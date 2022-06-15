# device's action and AP's action
from enum import(IntEnum, unique)
from utils import*
from parameter import*

@unique
class D_State(IntEnum):
    init = 1
    connected = 2
    detached = 3
    handover = 4
    search = 5

@unique
class A_State(IntEnum):
    init = 1
    active = 2
    underpopulated = 3
    idle = 4
    transition = 5

# device's action(action a and action b are both set initially)
# c(device connect from one AP to another AP)
def connected_connected(device, ap_list):
    # choose next AP to connect but not the previous one
    selected_ap = find_ap(device, ap_list)
    if device.ap != None:
        device.ap.user.remove(device)         
        device_connect(device, selected_ap)
# d
def connected_detached(device, _):
    device_disconnect(device)
    device.timer = d_state_timer_detached
    device.state = D_State.detached
# e
def detached_connected(device, ap_list):
    selected_ap = find_ap(device, ap_list)
    if selected_ap != None:  
        device_connect(device, selected_ap)
        device.state = D_State.connected
        device.timer = float('inf')
# f
def detached_search(device, _):
    device.timer = d_state_timer_search
    device.state = D_State.search
# g
def search_detached(device, _):
    device.timer = d_state_timer_detached
    device.state = D_State.detached
# h
def search_connected(device, ap_list):
    dis = float('inf')
    selected_ap = None
    for ap in ap_list:
        # check if there exist avialable active AP
        if ap.state == A_State.active:
            if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(ap.power) and ap != device.ap: # all AP that cover the device
                if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                    dis = distance((device.x, device.y), (ap.x, ap.y))
                    selected_ap = ap
        # for idle AP, try power with p_max and check if exist idle AP convering detached device
        elif ap.state == A_State.idle and ap.timer == 0:
            if distance((device.x, device.y), (ap.x, ap.y)) < range_decode(p_max) and ap != device.ap:
                if distance((device.x, device.y), (ap.x, ap.y)) < dis and ap.type == device.type and len(ap.user) <= ap.upperbound:
                    dis = distance((device.x, device.y), (ap.x, ap.y))
                    selected_ap = ap
    if selected_ap.state == A_State.active:
        device_connect(device, selected_ap)
        device.state = D_State.connected
        device.timer = float('inf')
    # if ap is idle, allocate all resource in AP action, not here. And change device state in AP action
    elif selected_ap.state == A_State.idle:
        device.selected = selected_ap

# i
def connected_handover(device, _):
    device.timer = d_state_timer_handover
    device.state = D_State.handover
# j
def handover_connected(device, ap_list):
    selected_ap = find_ap(device, ap_list)
    if selected_ap != None: 
        if selected_ap != device.ap:
            device.ap.user.remove(device)
            device_connect(device, selected_ap)
            device.state = D_State.connected
            device.timer = float('inf')
        else:
            device.timer = float('inf')
            device.state = D_State.connected
# k
def handover_detached(device, _):
    device_disconnect(device)
    device.timer = d_state_timer_detached
    device.state = D_State.detached

# AP's action(action a and action b are both set initially)
# c is in information center(when 30s timers up, update ap's attribute)

# d
def active_underpopulated(ap, _, __):
    ap.timer = a_state_timer_underpopulate
    ap.state = A_State.underpopulated
# e
def underpopulated_active(ap, _, __):
    ap.timer = float('inf')
    ap.state = A_State.active
# f
def idle_active(ap, ap_list, device_list):
    for device in device_list:
        if device.selected == ap and device.state == D_State.search and distance((device.x, device.y), (ap.x, ap.y)) < range_decode(p_max) and ap.type == device.type and len(ap.user) <= ap.upperbound:
            ap.power_change(p_max, ap_list)
            select_channel(ap, ap_list)
            power_adjustment(ap, ap_list)
            device_connect(device, ap)
            device.state = D_State.connected
            device.selected = None
            device.timer = float('inf')
    ap.state = A_State.active
    ap.timer = float('inf')
# g
def active_idle(ap, ap_list, __):
    for user in ap.user:
        device_connect(user, find_other_ap(user, ap_list))
        ap.user.remove(user)
    ap.power_change(0, ap_list)
    ap.channel = 0
    ap.state = A_State.idle
    ap.timer = a_state_timer_idle
# h
def underpopulated_idle(ap, ap_list, _):
    for user in ap.user:
        assert(find_other_ap(user, ap_list) != None) # 當find_other_ap==None時會報錯
        device_connect(user, find_other_ap(user, ap_list))
        ap.user.remove(user)
    ap.power_change(0, ap_list)
    ap.channel = 0
    ap.state = A_State.idle
    ap.timer = a_state_timer_idle
# i
def idle_idle(ap, _, __):
    ap.timer = a_state_timer_idle
# j
def active_transition(ap, ap_list, __):
    ap.upperbound = transition_upperbound
# k
def transition_active(ap, ap_list, __):
    if ap.type == Type.throughput:
        ap.upperbound =  upperbound_throughput
    elif ap.type == Type.delay:
        ap.upperbound =  upperbound_delay