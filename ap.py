from enum import(IntEnum, unique)
from parameter import*
from utils import*
from action import*

class AP:
    def __init__(self, x, y, id, type_ap):
        self.x = x
        self.y = y
        self.power = 0
        self.channel = 0
        self.user = []
        self.id = id
        self.type = type_ap
        self.timer = 0
        self.state = A_State.init
        self.cci = 0
        self.neighbor = []
        self.pre_neighbor = []
        self.interference_range = 0
        self.communication_range = 0
        self.throughput = 0
        self.lowerbound = 0
        self.upperbound = 0

    def power_change(self, power, ap_list):
        self.power = power
        self.interference_range = range_interference(power)
        self.communication_range = range_decode(power)
        self.neighbor_cal(ap_list)

    # define neighbor ap(power!=0) as if there exist ap in interference range
    def neighbor_cal(self, ap_list):
        for ap in ap_list:
            if ap not in self.neighbor and self.interference_range + ap.interference_range >= distance((self.x, self.y), (ap.x, ap.y)) and ap != self and ap.power!=0 and self.power!=0:
                self.neighbor.append(ap)
                ap.neighbor.append(self)
        for neighbor in self.neighbor:
            if self.interference_range + neighbor.interference_range < distance((self.x, self.y), (neighbor.x, neighbor.y)) or neighbor.power!=0 or self.power!=0:
                self.neighbor.remove(neighbor)
                neighbor.neighbor.remove(self)

    def adduser(self, users):
        if users not in self.user:
            self.user.append(users)

    def cci_calculation(self):
        self.cci = 0
        for neighbor in self.neighbor:
            for ch in ch_dic[neighbor.channel]:
                if ch == self.channel:
                    self.cci = self.cci + 1

    def state_change(self, ap_list, device_list):
        flag = False
        next_state = None
        if self.timer == 0:
            if self.state == A_State.active:
                pass
            elif self.state == A_State.underpopulated:
                other_ap_flag = False
                for user in self.user:
                    if find_other_ap(user, ap_list) == None:
                        other_ap_flag = True
                        break
                if other_ap_flag:
                    next_state = A_State.active
                else:   
                    next_state = A_State.idle
                flag = True
            elif self.state == A_State.idle:
                idle_flag = False
                for device in device_list:
                    if device.selected == self and device.state == D_State.search and distance((device.x, device.y), (self.x, self.y)) < range_decode(p_max) and self.type == device.type and len(self.user) <= self.upperbound:
                        idle_flag = True
                        break
                if idle_flag:
                    next_state = A_State.active
                else:
                    next_state = A_State.idle
                flag = True

        if self.state == A_State.active:
            if len(self.user) == 0:
                next_state = A_State.idle
                flag = True
            elif len(self.user) < self.lowerbound and len(self.user) != 0:
                next_state = A_State.underpopulated
                flag = True
            if self.type == Type.throughput:
                for device in device_list:
                    if device.type == Type.delay and device.state == D_State.search and distance((device.x, device.y), (self.x, self.y)) < range_decode(self.power) and len(self.user) < transition_upperbound:
                        next_state = A_State.transition
                        flag = True
        
        if self.state == A_State.transition:
            transition_flag = False
            for user in self.user:
                if user.type == Type.delay:
                    transition_flag = True
                    break
            if not transition_flag:
                next_state = A_State.active
                flag = True
        return flag, next_state

    def action(self, next_state, ap_list, device_list):
        transition_table = {
            A_State.active : {
                A_State.underpopulated : active_underpopulated, 
                A_State.idle : active_idle,
                A_State.transition : active_transition
            }, 
            A_State.underpopulated : {
                A_State.active : underpopulated_active, 
                A_State.idle : underpopulated_idle
            }, 
            A_State.transition : {
                A_State.active : transition_active 
            },
            A_State.idle : {
                A_State.active : idle_active, 
                A_State.idle : idle_idle
            }
        }
        transition_table[self.state][next_state](self, ap_list, device_list)