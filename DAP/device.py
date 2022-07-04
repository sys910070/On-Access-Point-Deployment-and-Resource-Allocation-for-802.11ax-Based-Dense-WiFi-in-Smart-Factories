from os import environ
import random
from matplotlib.pyplot import flag
from parameter import*
from action import*
from utils import*


class DEVICE:
    def __init__(self, x, y, id, type_device):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.power = 0
        self.channel = 0
        self.id = id
        self.type = type_device
        self.state = D_State.init
        self.ap = None
        self.throughput = 0
        self.timer = float('inf')
        self.selected = None
        self.dis = 0
        self.throughput = 0

    def move(self):
        if self.type == 2:
            if factory_environment == 'no_obstacle':
                while True:
                    self.vx = random.randint(-5, 5)
                    self.vy = random.randint(-5, 5)
                    if boundary_no_obstacle(self.x + self.vx, self.y + self.vy):
                        self.x = self.x + self.vx
                        self.y = self.y + self.vy
                        break
            elif factory_environment == 'symmetric_obstacle':
                while True:
                    self.vx = random.randint(-5, 5)
                    self.vy = random.randint(-5, 5)
                    if boundary_symmetric_obstacle(self.x + self.vx, self.y + self.vy):
                        self.x = self.x + self.vx
                        self.y = self.y + self.vy
                        break
            elif factory_environment == 'asymmetric_obstacle':
                while True:
                    self.vx = random.randint(-5, 5)
                    self.vy = random.randint(-5, 5)
                    if boundary_asymmetric_obstacle(self.x + self.vx, self.y + self.vy):
                        self.x = self.x + self.vx
                        self.y = self.y + self.vy
                        break

    def dis_cal(self):
        if self.ap == None:
            self.dis = 0
        else:
            self.dis = distance((self.x, self.y), (self.ap.x, self.ap.y))

    def throughput_cal(self):
        if self.ap != None:
            self.throughput = (self.ap.throughput*(T_ULPPDU+T_DLPPDU)/((self.ap.cci+1)*(T_UL+T_DL)))/len(self.ap.user)
            self.ap.user_throughput = self.throughput
        else:
            self.throughput = 0

    def state_change(self, ap_list):
        flag = False
        next_state = None
        if self.ap != None:
            # device move out of range
            if self.state == D_State.connected:
                if distance((self.x, self.y), (self.ap.x, self.ap.y)) > range_decode(self.ap.power):
                    if find_active_ap(self, ap_list) != None:
                        next_state = D_State.connected
                        flag = True
                    else:
                        next_state = D_State.detached
                        flag = True
                # overlapped BSS
                else:
                    for ap in ap_list:
                        # in ap's decode range
                        if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(ap.power):
                            if ap.type == self.type and distance((self.x, self.y), (self.ap.x, self.ap.y)) > distance((self.x, self.y), (ap.x, ap.y)):
                                next_state = D_State.handover
                                flag = True
                                break
            if self.state == D_State.handover:
                if find_active_ap(self, ap_list) != None:
                    next_state = D_State.connected
                    flag = True
                else:
                    next_state = D_State.detached
                    flag = True

        # device in search state
        if self.state == D_State.search and self.timer !=0:
            dis = float('inf')
            selected_ap = None
            for ap in ap_list:
                # check if there exist avialable active AP or idle AP but timer needs to be 0
                if ap.state == A_State.idle and ap.timer == 0:
                    if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(p_max) and ap != self.ap:
                        if distance((self.x, self.y), (ap.x, ap.y)) < dis and ap.type == self.type and len(ap.user) <= ap.upperbound:
                            dis = distance((self.x, self.y), (ap.x, ap.y))
                            selected_ap = ap
                # for idle AP, try power with p_max and check if exist idle AP convering detached device
                else:
                    if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(ap.power) and ap != self.ap: # all AP that cover the device
                        if distance((self.x, self.y), (ap.x, ap.y)) < dis and ap.type == self.type and len(ap.user) <= ap.upperbound:
                            dis = distance((self.x, self.y), (ap.x, ap.y))
                            selected_ap = ap
            if selected_ap != None:
                next_state = D_State.connected
                flag = True

        # device timer expired
        if self.timer == 0:
            if self.state == D_State.detached:
                if find_active_ap(self, ap_list) != None:  
                    next_state = D_State.connected
                    flag = True
                else:
                    next_state = D_State.search
                    flag = True
            elif self.state == D_State.handover:
                if find_active_ap(self, ap_list) != None:  
                    next_state = D_State.connected
                    flag = True
                else:
                    next_state = D_State.detached
                    flag = True
            elif self.state == D_State.search:
                if find_active_ap(self, ap_list) != None:  
                    next_state = D_State.connected
                    flag = True
                else:
                    next_state = D_State.detached
                    flag = True
                    
        return flag, next_state
        
    def action(self, next_state, ap_list):
        transition_table = {
            D_State.connected : {
                D_State.connected : connected_connected, 
                D_State.detached : connected_detached, 
                D_State.handover : connected_handover
            }, 
            D_State.detached : {
                D_State.connected : detached_connected, 
                D_State.search : detached_search
            }, 
            D_State.handover : {
                D_State.connected : handover_connected, 
                D_State.detached : handover_detached
            },
            D_State.search : {
                D_State.connected : search_connected, 
                D_State.detached : search_detached
            }
        }
        transition_table[self.state][next_state](self, ap_list)

    def ok(self):
        if self.ap == None:
            if self.state == D_State.connected:
                print('device', self.id)
                return False
            if self.state == D_State.handover:
                print('device', self.id)
                return False                
        else:
            if self.state == D_State.search:
                print('device', self.id)
                return False
            if self.state == D_State.detached:
                print('device', self.id)
                return False                
        return True