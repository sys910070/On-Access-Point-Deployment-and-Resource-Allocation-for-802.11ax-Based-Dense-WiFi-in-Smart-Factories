from enum import(IntEnum, unique)
from parameter import*
from utils import*
from action import*
import math

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
        self.neighbor_decode = []
        self.pre_neighbor = []
        self.interference_range = 0
        self.communication_range = 0
        self.throughput = 0
        self.user_throughput = 0
        self.lowerbound = 0
        self.upperbound = 0
        self.ranking = 0
        self.partner = None

    def power_change(self, power, ap_list):
        self.power = power
        self.interference_range = range_interference(power)
        self.communication_range = range_decode(power)
        if len(self.user) != 0:
            for user in self.user:
                user.power = self.power
        self.neighbor_cal(ap_list)

    def throughput_cal(self):
        if self.power != 0:
            self.throughput = 0.9683738202073339*ch_id_to_bw[self.channel]*math.log2(1+(self.power-NOISE))/(self.cci+1)
        else:
            self.throughput = 0
            self.user_throughput = 0
            
    # def throughput_cal(self):
    #     if self.power != 0:
    #         self.throughput = ch_id_to_bw[self.channel]*math.log2(1+(self.power-NOISE))
    #     else:
    #         self.throughput = 0
    #         self.user_throughput = 0
    
    # define neighbor_decode ap(power!=0) as if there exist ap in decode range
    # define neighbor ap(power!=0) as if there exist ap in interference range
    def neighbor_cal(self, ap_list):
        list_remove_neighbor_decode = []
        for ap in ap_list:
            if ap not in self.neighbor_decode and self.communication_range + ap.communication_range >= distance((self.x, self.y), (ap.x, ap.y)) and ap != self and ap.power!=0 and self.power!=0:
                self.neighbor_decode.append(ap)
                ap.neighbor_decode.append(self)
        for neighbor_decode in self.neighbor_decode:
            if self.communication_range + neighbor_decode.communication_range < distance((self.x, self.y), (neighbor_decode.x, neighbor_decode.y)) or neighbor_decode.power == 0 or self.power == 0:
                list_remove_neighbor_decode.append(neighbor_decode)
        for neighbor_decode in list_remove_neighbor_decode:
            self.neighbor_decode.remove(neighbor_decode)
            neighbor_decode.neighbor_decode.remove(self) 

        list_remove_neighbor = []
        for ap in ap_list:
            if ap not in self.neighbor and self.interference_range + ap.interference_range >= distance((self.x, self.y), (ap.x, ap.y)) and ap != self and ap.power!=0 and self.power!=0:
                self.neighbor.append(ap)
                ap.neighbor.append(self)
        for neighbor in self.neighbor:
            if self.interference_range + neighbor.interference_range < distance((self.x, self.y), (neighbor.x, neighbor.y)) or neighbor.power == 0 or self.power == 0:
                list_remove_neighbor.append(neighbor)
        for neighbor in list_remove_neighbor:
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
        if self.state == A_State.active:
            if len(self.user) == 0:
                next_state = A_State.idle
                flag = True
            elif len(self.user) < self.lowerbound and len(self.user) != 0:
                next_state = A_State.underpopulated
                flag = True
        
        if self.state == A_State.underpopulated and self.timer != 0:
            user_count = 0
            if selected_device_check(self, device_list):
                for device in device_list:
                    for user in self.user:
                        if device.selected == self and device != user:
                            user_count += 1
            if len(self.user)+user_count == 0:
                next_state = A_State.idle
                flag = True
            elif len(self.user)+user_count >= self.lowerbound:
                next_state = A_State.active
                flag = True

        if self.timer == 0:
            user_count = 0
            if self.state == A_State.underpopulated:
                # need to know if there are device going to connect to this ap first
                if selected_device_check(self, device_list):
                    for device in device_list:
                        for user in self.user:
                            if device.selected == self and device != user:
                                user_count += 1     
                    if user_count+len(self.user) >= self.lowerbound:
                        flag = True
                        next_state = A_State.active
                    else:
                        flag = True
                        next_state = A_State.underpopulated
                else:
                    other_ap_flag = False
                    dic = {}                    
                    for user in self.user:
                        selected_ap = find_other_active_ap(user, ap_list)
                        if selected_ap != None:
                            if selected_ap.id not in dic:
                                dic[selected_ap.id] = len(selected_ap.user)
                            dic[selected_ap.id] += 1 
                        if selected_ap == None or dic[selected_ap.id]>selected_ap.upperbound:
                            other_ap_flag = True
                            break
                    if other_ap_flag:
                        if len(self.user) < self.lowerbound:
                            next_state = A_State.underpopulated
                        else: 
                            next_state = A_State.active
                    else:   
                        next_state = A_State.idle
                    flag = True
            elif self.state == A_State.idle:
                idle_flag = False
                for device in device_list:
                    if device.selected == self and device.state == D_State.search and distance((device.x, device.y), (self.x, self.y)) < range_decode(p_max) and self.type == device.type and len(self.user) <= self.upperbound:
                        idle_flag = True
                        user_count += 1
                if idle_flag:
                    if user_count < self.lowerbound:
                        next_state = A_State.underpopulated
                    else:
                        next_state = A_State.active
                else:
                    next_state = A_State.idle
                flag = True
        return flag, next_state

    def action(self, next_state, ap_list, device_list):               
        transition_table = {
            A_State.active : {
                A_State.underpopulated : active_underpopulated, 
                A_State.idle : active_idle,
            }, 
            A_State.underpopulated : {
                A_State.active : underpopulated_active, 
                A_State.idle : underpopulated_idle, 
                A_State.underpopulated : underpopulated_underpopulated
            }, 
            A_State.idle : {
                A_State.active : idle_active, 
                A_State.underpopulated : idle_underpopulated, 
                A_State.idle : idle_idle
            }
        }
        transition_table[self.state][next_state](self, ap_list, device_list)

    def ok(self):
        if len(self.user) == 0:
            if self.state != A_State.idle:
                print('ap', self.id, 'idle')
                return False
        elif len(self.user) < self.lowerbound and len(self.user) != 0:
            if self.state != A_State.underpopulated:
                print('ap', self.id, 'underpopulated')
                return False
        else:
            if self.state != A_State.active:
                print('ap', self.id, 'active or transition')
                return False
        return True