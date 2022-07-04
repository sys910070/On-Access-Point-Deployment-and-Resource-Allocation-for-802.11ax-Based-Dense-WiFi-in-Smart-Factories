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
        self.cci = 0
        self.state = A_State.random
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
            self.throughput = ch_id_to_bw[self.channel]*math.log2(1+(self.power-NOISE))
        else:
            self.throughput = 0
            self.user_throughput = 0
    
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

    def action(self, next_state, ap_list, device_list):               
        transition_table = {
            A_State.active : {
                A_State.underpopulated : active_underpopulated, 
                A_State.idle : active_idle,
                A_State.transition : active_transition
            }, 
            A_State.underpopulated : {
                A_State.active : underpopulated_active, 
                A_State.idle : underpopulated_idle, 
                A_State.underpopulated : underpopulated_underpopulated
            }, 
            A_State.transition : {
                A_State.active : transition_active 
            },
            A_State.idle : {
                A_State.active : idle_active, 
                A_State.underpopulated : idle_underpopulated, 
                A_State.idle : idle_idle
            }
        }
        transition_table[self.state][next_state](self, ap_list, device_list)